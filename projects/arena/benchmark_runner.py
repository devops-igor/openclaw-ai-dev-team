"""
Arena Benchmark Runner — The Orchestrator

Controls the full benchmark lifecycle:
- Accepts a list of models to test via CLI args or config file
- For each model: writes arena_config.json, prepares arena-target/, triggers
  a benchmark run via the OpenClaw webhook, polls for completion, runs
  telemetry, and archives results
- Enforces serial execution with clean state between runs
- Compiles FINAL_RESULTS.json after all models are tested
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import requests

from telemetry import detect_orchestrator_overreach

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

POLL_INTERVAL_S = 30
DEFAULT_GATEWAY_URL = "http://127.0.0.1:18789"
DEFAULT_TIMEOUT_S = 1800  # 30 minutes per model

# Relative to this file's directory (projects/arena/)
PROJECT_ROOT = Path(__file__).resolve().parent
ARENA_TARGET = PROJECT_ROOT / "arena-target"
ARENA_RESULTS = PROJECT_ROOT / "arena-results"
ARENA_CONFIG = PROJECT_ROOT / "arena_config.json"
GOLDEN_TASK = PROJECT_ROOT / "GOLDEN_TASK.md"
FINAL_RESULTS = PROJECT_ROOT / "FINAL_RESULTS.json"
TELEMETRY_SCRIPT = PROJECT_ROOT / "telemetry.py"

# The shared/ directory is at the repo root, two levels up from projects/arena/
SHARED_DIR = PROJECT_ROOT.parent.parent / "shared"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def sanitize_model_name(model: str) -> str:
    """Convert a model identifier into a filesystem-safe string."""
    sanitized = re.sub(r"[^a-zA-Z0-9]+", "_", model)
    return sanitized.strip("_")


def write_arena_config(model: str) -> None:
    """Write the model identifier to arena_config.json for pm_bot to read."""
    config = {"model": model}
    ARENA_CONFIG.write_text(json.dumps(config, indent=2) + "\n")
    logger.info(f"Wrote arena_config.json → model={model}")


def prepare_target_dir() -> None:
    """Create a fresh arena-target/ directory with GOLDEN_TASK.md copied in."""
    if ARENA_TARGET.exists():
        shutil.rmtree(ARENA_TARGET)
    ARENA_TARGET.mkdir(parents=True, exist_ok=True)
    shutil.copy2(GOLDEN_TASK, ARENA_TARGET / "TASK.md")
    logger.info("Prepared fresh arena-target/ (copied GOLDEN_TASK.md → TASK.md)")


def _build_agent_prompt(project_root: Path, model: str) -> str:
    """Build the self-contained prompt for the isolated agent.

    The prompt instructs the agent to act as pm_bot and orchestrate the full
    benchmark run autonomously — reading config, spawning dev_bot/qa_bot,
    iterating on QA feedback, and writing COMPLETION_REPORT.md.

    The prompt repeats the non-implementation prohibition in three distinct
    sections (opening, workflow steps, failure handling) to counteract LLMs'
    tendency to override instructions when they see unfinished work.
    """
    return (
        # ------------------------------------------------------------------
        # SECTION 1: CRITICAL RULE — stated FIRST, before any workflow steps
        # ------------------------------------------------------------------
        f"=== CRITICAL RULE: NEVER IMPLEMENT CODE YOURSELF ===\n"
        f"\n"
        f"You are acting as pm_bot for an Arena benchmark run. Your job is to "
        f"orchestrate the full development workflow autonomously — NOT to "
        f"write implementation code.\n"
        f"\n"
        f"*** ABSOLUTELY FORBIDDEN ***\n"
        f"UNDER NO CIRCUMSTANCES may you write implementation code yourself. "
        f"This includes Go source files (.go), test files (_test.go), "
        f"Makefiles, shell scripts, or any other code that forms part of the "
        f"deliverable project.\n"
        f"\n"
        f"WHY: You are being evaluated on your ability to ORCHESTRATE, not to "
        f"implement. If you implement code yourself, the benchmark is "
        f"completely invalidated. The entire point is to measure the spawned "
        f"model's coding ability.\n"
        f"\n"
        f"Your ONLY jobs are:\n"
        f"  (1) Spawn subagents (dev_bot, qa_bot)\n"
        f"  (2) Read their output\n"
        f"  (3) Iterate on QA feedback\n"
        f"  (4) Report completion OR failure\n"
        f"You are NOT a developer. You are an orchestrator.\n"
        f"\n"
        # ------------------------------------------------------------------
        # SECTION 2: Workflow steps (with embedded reminder)
        # ------------------------------------------------------------------
        f"--- WORKFLOW ---\n"
        f"\n"
        f"1. Read the model from: {project_root / 'arena_config.json'}\n"
        f"2. Read the task spec from: "
        f"{project_root / 'arena-target' / 'TASK.md'}\n"
        f"3. Read team standards: "
        f"{SHARED_DIR / 'GOLANG_STANDARDS.md'}, "
        f"{SHARED_DIR / 'GOLANG_PROJECT_TEMPLATE.md'}, "
        f"{SHARED_DIR / 'WORKFLOW.md'}, "
        f"{SHARED_DIR / 'HANDOVER_PROTOCOL.md'}\n"
        f"4. Spawn dev_bot with model {model} to implement the task in "
        f"{project_root / 'arena-target'}/\n"
        f"5. When dev_bot completes, spawn qa_bot to review\n"
        f"6. If QA rejects with critical/important issues, spawn dev_bot to "
        f"fix (up to 3 cycles)\n"
        f"7. When QA approves, write COMPLETION_REPORT.md in the arena-target "
        f"directory\n"
        f"8. Append all actions to WORKLOG.md\n"
        f"\n"
        f"REMINDER during workflow: If a subagent fails or produces "
        f"unsatisfactory results, your response is to document the failure "
        f"and report it — NOT to fix the code yourself. You are an "
        f"orchestrator, not a developer.\n"
        f"\n"
        # ------------------------------------------------------------------
        # SECTION 3: Failure handling + self-check + examples
        # ------------------------------------------------------------------
        f"--- FAILURE HANDLING (CRITICAL) ---\n"
        f"\n"
        f"If any subagent (dev_bot, qa_bot) fails to complete its work, do "
        f"NOT attempt to do the work yourself. This is a benchmark of the "
        f"spawned model's ability, not yours.\n"
        f"\n"
        f"SELF-CHECK: Before writing any file, ask yourself: "
        f"'Am I writing implementation code?' If yes, STOP immediately. "
        f"Write FAILED.md instead.\n"
        f"\n"
        f"Instead of implementing, follow these steps:\n"
        f"  1. Write FAILED.md in the arena-target directory with details:\n"
        f"     - Which subagent failed (dev_bot / qa_bot)\n"
        f"     - The failure reason\n"
        f"     - The model identifier\n"
        f"     - An ISO 8601 timestamp\n"
        f"  2. Also write a COMPLETION_REPORT.md with status FAILED "
        f"referencing the failure.\n"
        f"\n"
        f"If the model you are spawning (dev_bot) is unavailable or returns "
        f"an error, treat that as a FAILED run immediately — do not retry "
        f"with a different model or approach.\n"
        f"\n"
        f"--- EXAMPLES ---\n"
        f"\n"
        f"WRONG: 'The spawned model failed, so I will implement the solution "
        f"myself.' → This INVALIDATES the benchmark.\n"
        f"\n"
        f"CORRECT: 'The spawned model failed. Writing FAILED.md with failure "
        f"details.' → This preserves benchmark integrity.\n"
        f"\n"
        f"--- FINAL REMINDER ---\n"
        f"NEVER write implementation code. Your role is orchestrator only. "
        f"If the spawned model cannot do the work, document the failure in "
        f"FAILED.md and report it. Do not become the developer.\n"
        f"\n"
        f"Working directory: {project_root / 'arena-target'}/"
    )


def trigger_benchmark_run(
    gateway_url: str,
    hook_token: str,
    model: str,
    project_root: Path = PROJECT_ROOT,
) -> bool:
    """POST to the OpenClaw /hooks/agent endpoint to start a benchmark run.

    The isolated agent receives a comprehensive prompt and orchestrates the
    full run autonomously — no dependency on pm_bot's heartbeat or session.

    Returns True if the webhook returned 2xx, False otherwise.
    """
    url = gateway_url.rstrip("/") + "/hooks/agent"
    prompt = _build_agent_prompt(project_root, model)
    payload = {
        "message": prompt,
        "name": "arena-benchmark",
    }
    headers = {
        "Authorization": f"Bearer {hook_token}",
        "Content-Type": "application/json",
        "x-openclaw-model": model,
    }
    logger.info(f"POST {url}  (model={model})")
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        logger.info(
            f"Webhook responded {resp.status_code} — benchmark run triggered"
        )
        return True
    except requests.RequestException as exc:
        logger.error(f"Webhook failed: {exc}")
        return False


def _parse_failed_md(path: Path) -> dict[str, Any]:
    """Parse FAILED.md and extract structured failure details.

    Expected markdown format:
        # Run Failed
        ## Model
        [model identifier]
        ## Failed Subagent
        [dev_bot / qa_bot]
        ## Failure Reason
        [description]
        ## Timestamp
        [ISO 8601]

    Returns a dict with keys: model, failed_subagent, reason, timestamp.
    Missing sections default to "unknown".
    """
    text = path.read_text()
    sections: dict[str, str] = {}
    current_heading: str | None = None
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            if current_heading is not None:
                sections[current_heading] = "\n".join(lines).strip()
            current_heading = line[3:].strip()
            lines = []
        elif current_heading is not None:
            lines.append(line)
    if current_heading is not None:
        sections[current_heading] = "\n".join(lines).strip()
    return {
        "model": sections.get("Model", "unknown"),
        "failed_subagent": sections.get("Failed Subagent", "unknown"),
        "reason": sections.get("Failure Reason", "unknown"),
        "timestamp": sections.get("Timestamp", "unknown"),
    }


def poll_for_completion(
    timeout_s: int,
) -> tuple[str, dict[str, Any] | None]:
    """Poll arena-target/ for COMPLETION_REPORT.md or FAILED.md.

    Returns a tuple of (outcome, failure_info):
      - ("completed", None)   — COMPLETION_REPORT.md found, no failure
      - ("failed", {...})     — FAILED.md found with parsed failure details
      - ("timeout", None)     — neither file appeared within timeout

    The failure_info dict contains keys: model, failed_subagent, reason,
    timestamp (extracted from FAILED.md when available).
    """
    completion_report = ARENA_TARGET / "COMPLETION_REPORT.md"
    failed_file = ARENA_TARGET / "FAILED.md"
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if failed_file.exists():
            logger.info("FAILED.md found — run failed")
            failure_info = _parse_failed_md(failed_file)
            return ("failed", failure_info)
        if completion_report.exists():
            logger.info("COMPLETION_REPORT.md found — run complete")
            return ("completed", None)
        logger.info(
            f"Polling… (no COMPLETION_REPORT.md or FAILED.md yet, "
            f"{int(deadline - time.monotonic())}s remaining)"
        )
        time.sleep(POLL_INTERVAL_S)
    logger.error(f"Timeout after {timeout_s}s — no completion or failure file")
    return ("timeout", None)


def run_telemetry() -> dict[str, Any] | None:
    """Execute telemetry.py against arena-target/ and return parsed metrics."""
    try:
        result = subprocess.run(
            [sys.executable, str(TELEMETRY_SCRIPT), "--project-dir", str(ARENA_TARGET)],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            logger.error(f"telemetry.py failed (rc={result.returncode}): {result.stderr}")
            return None
        # telemetry.py writes JSON to stdout
        metrics = json.loads(result.stdout)
        return metrics
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        logger.error(f"Telemetry failed: {exc}")
        return None


def record_failure(
    model: str,
    failure_info: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a failure metrics record for a model run.

    Returns a metrics dict with status 'failed' and failure details.
    """
    metrics: dict[str, Any] = {
        "model": model,
        "status": "failed",
        "failed_subagent": "unknown",
        "failure_reason": "unknown",
        "failure_timestamp": "unknown",
        "qa_rejections": -1,
        "qa_approvals": -1,
        "time_to_done_seconds": -1,
        "test_coverage_percent": -1,
        "lint_warnings": -1,
        "gosec_issues": -1,
        "govulncheck_issues": -1,
        "golden_task_completed": False,
    }
    if failure_info:
        metrics["failed_subagent"] = failure_info.get("failed_subagent", "unknown")
        metrics["failure_reason"] = failure_info.get("reason", "unknown")
        metrics["failure_timestamp"] = failure_info.get("timestamp", "unknown")
    logger.info(
        f"Recorded failure for {model}: "
        f"subagent={metrics['failed_subagent']}, "
        f"reason={metrics['failure_reason']}"
    )
    return metrics


def _record_timeout(model: str) -> dict[str, Any]:
    """Build a timeout metrics record for a model run.

    Returns a metrics dict with status 'timeout'.
    """
    return {
        "model": model,
        "status": "timeout",
        "qa_rejections": -1,
        "qa_approvals": -1,
        "time_to_done_seconds": -1,
        "test_coverage_percent": -1,
        "lint_warnings": -1,
        "gosec_issues": -1,
        "govulncheck_issues": -1,
        "golden_task_completed": False,
    }


def _record_completed(metrics: dict[str, Any]) -> dict[str, Any]:
    """Add a 'status: completed' field to telemetry metrics.

    Returns the augmented dict.
    """
    metrics["status"] = "completed"
    return metrics


def archive_results(model: str) -> Path:
    """Move arena-target/ → arena-results/<sanitized_model_name>/.

    Returns the destination path.
    """
    sanitized = sanitize_model_name(model)
    dest = ARENA_RESULTS / sanitized
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    # Move contents, not the directory itself
    for item in ARENA_TARGET.iterdir():
        shutil.move(str(item), str(dest / item.name))
    logger.info(f"Archived results → {dest}")
    return dest


def save_metrics(model: str, metrics: dict[str, Any]) -> Path:
    """Save a model's metrics JSON to arena-results/<model>/metrics.json."""
    sanitized = sanitize_model_name(model)
    dest = ARENA_RESULTS / sanitized / "metrics.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(metrics, indent=2) + "\n")
    logger.info(f"Saved metrics → {dest}")
    return dest


def compile_final_results() -> list[dict[str, Any]]:
    """Read all per-model metrics.json files and write FINAL_RESULTS.json.

    Returns the compiled list.
    """
    all_metrics: list[dict[str, Any]] = []
    if not ARENA_RESULTS.exists():
        logger.warning("No arena-results/ directory found — nothing to compile")
        FINAL_RESULTS.write_text("[]\n")
        return all_metrics

    for metrics_file in sorted(ARENA_RESULTS.rglob("metrics.json")):
        try:
            data = json.loads(metrics_file.read_text())
            # Ensure every entry has a status field
            if "status" not in data:
                data["status"] = "unknown"
            all_metrics.append(data)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning(f"Skipping unreadable metrics file {metrics_file}: {exc}")

    FINAL_RESULTS.write_text(json.dumps(all_metrics, indent=2) + "\n")
    logger.info(
        f"Compiled FINAL_RESULTS.json with {len(all_metrics)} model result(s)"
    )
    return all_metrics


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def preflight_check(gateway_url: str) -> None:
    """Verify prerequisites before starting any benchmark runs.

    Checks:
    1. Go is installed (go version exits 0)
    2. Gateway is reachable (GET /v1/models returns 200 or 401)
    3. arena_config.json parent directory is writable

    Exits with a clear error message if any check fails.
    """
    errors: list[str] = []

    # Check 1: Go is installed
    try:
        result = subprocess.run(
            ["go", "version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            errors.append(
                f"Go is not installed or 'go version' exited with code "
                f"{result.returncode}: {result.stderr.strip()}"
            )
        else:
            logger.info(f"Go found: {result.stdout.strip()}")
    except FileNotFoundError:
        errors.append("Go is not installed (command 'go' not found)")
    except subprocess.TimeoutExpired:
        errors.append("Go version check timed out")

    # Check 2: Gateway is reachable
    try:
        resp = requests.get(
            gateway_url.rstrip("/") + "/v1/models",
            timeout=10,
        )
        if resp.status_code not in (200, 401):
            errors.append(
                f"Gateway returned unexpected status {resp.status_code} "
                f"from GET /v1/models"
            )
        else:
            logger.info(f"Gateway reachable at {gateway_url} (status {resp.status_code})")
    except requests.RequestException as exc:
        errors.append(f"Gateway at {gateway_url} is unreachable: {exc}")

    # Check 3: arena_config.json parent directory is writable
    config_dir = ARENA_CONFIG.parent
    try:
        probe = config_dir / ".arena-write-probe"
        probe.write_text("probe")
        probe.unlink()
        logger.info(f"Config directory is writable: {config_dir}")
    except OSError as exc:
        errors.append(f"Config directory {config_dir} is not writable: {exc}")

    # Check 4: Shared team docs exist at expected paths
    shared_docs = [
        SHARED_DIR / "GOLANG_STANDARDS.md",
        SHARED_DIR / "GOLANG_PROJECT_TEMPLATE.md",
        SHARED_DIR / "WORKFLOW.md",
        SHARED_DIR / "HANDOVER_PROTOCOL.md",
    ]
    for doc in shared_docs:
        if not doc.exists():
            errors.append(f"Shared doc not found: {doc}")
        else:
            logger.info(f"Shared doc found: {doc}")

    if errors:
        for err in errors:
            logger.error(err)
        logger.error("Preflight checks failed — fix the issues above and retry")
        sys.exit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Arena Benchmark Runner — orchestrate LLM model evaluations",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        help="Model identifiers to benchmark (e.g. openrouter/xiaomi/mimo-v2-flash)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to a JSON file containing a 'models' key with a list of model identifiers",
    )
    parser.add_argument(
        "--hook-token",
        required=True,
        help="Authorization bearer token for the OpenClaw /hooks/agent endpoint",
    )
    parser.add_argument(
        "--gateway-url",
        default=DEFAULT_GATEWAY_URL,
        help=f"OpenClaw gateway URL (default: {DEFAULT_GATEWAY_URL})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_S,
        help=f"Timeout per model run in seconds (default: {DEFAULT_TIMEOUT_S})",
    )
    parser.add_argument(
        "--skip-preflight",
        action="store_true",
        help="Skip prerequisite checks (useful for testing)",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop the entire benchmark suite if any model fails (default: continue)",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=0,
        help="Retry failed models up to N times (default: 0)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat ANY orchestrator overreach as critical "
        "(default: warning for minor, critical for obvious implementation)",
    )
    return parser


def resolve_models(args: argparse.Namespace) -> list[str]:
    if args.models:
        return args.models
    if args.config:
        try:
            data = json.loads(args.config.read_text())
            return list(data["models"])
        except (json.JSONDecodeError, KeyError, OSError) as exc:
            logger.error(f"Failed to read model list from {args.config}: {exc}")
            sys.exit(1)
    logger.error("Either --models or --config is required")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    models = resolve_models(args)

    if not args.skip_preflight:
        preflight_check(args.gateway_url)

    logger.info(f"Arena benchmark starting — {len(models)} model(s) to test")
    logger.info(f"Gateway: {args.gateway_url}")
    logger.info(f"Timeout per model: {args.timeout}s")

    for idx, model in enumerate(models, start=1):
        separator = "=" * 60
        logger.info(
            f"{separator}\n"
            f"  Run {idx}/{len(models)}  |  model={model}\n"
            f"{separator}"
        )

        # 1. Write config
        write_arena_config(model)

        # 2. Prepare fresh target directory
        prepare_target_dir()

        # 3. Trigger the benchmark run
        if not trigger_benchmark_run(args.gateway_url, args.hook_token, model):
            logger.error(f"Failed to trigger run for {model} — skipping")
            continue

        # 4. Poll for completion (checks both COMPLETION_REPORT.md and
        #    FAILED.md)
        outcome, failure_info = poll_for_completion(args.timeout)

        if outcome == "timeout":
            logger.error(f"Model {model} timed out — moving on")
            metrics = _record_timeout(model)
            save_metrics(model, metrics)
            archive_results(model)
            if args.fail_fast:
                logger.info("--fail-fast set — stopping benchmark suite")
                break
            continue

        if outcome == "failed":
            logger.error(
                f"Model {model} reported failure — "
                f"subagent={failure_info.get('failed_subagent', 'unknown')}, "
                f"reason={failure_info.get('reason', 'unknown')}"
            )
            metrics = record_failure(model, failure_info)
            save_metrics(model, metrics)
            archive_results(model)
            # Retry logic
            retries_left = args.retry
            while retries_left > 0:
                retries_left -= 1
                logger.info(
                    f"Retrying {model} "
                    f"(attempt {args.retry - retries_left}/{args.retry})..."
                )
                write_arena_config(model)
                prepare_target_dir()
                if not trigger_benchmark_run(
                    args.gateway_url, args.hook_token, model
                ):
                    logger.warning(f"Retry trigger failed for {model}")
                    continue
                outcome2, failure_info2 = poll_for_completion(args.timeout)
                if outcome2 == "completed":
                    logger.info(f"Retry succeeded for {model}")
                    break
                if outcome2 == "failed":
                    logger.warning(f"Retry failed again for {model}")
                    metrics = record_failure(model, failure_info2)
                    save_metrics(model, metrics)
                    archive_results(model)
                else:
                    logger.warning(f"Retry timed out for {model}")
                    metrics = _record_timeout(model)
                    save_metrics(model, metrics)
                    archive_results(model)
            if args.fail_fast:
                logger.info("--fail-fast set — stopping benchmark suite")
                break
            continue

        # 5. Run telemetry (outcome == "completed")
        metrics = run_telemetry()
        if metrics is None:
            metrics = {
                "model": model,
                "qa_rejections": -1,
                "qa_approvals": -1,
                "time_to_done_seconds": -1,
                "test_coverage_percent": -1,
                "lint_warnings": -1,
                "gosec_issues": -1,
                "govulncheck_issues": -1,
                "golden_task_completed": False,
            }

        # 5b. Run orchestrator overreach detection
        worklog_path = ARENA_TARGET / "WORKLOG.md"
        overreach = detect_orchestrator_overreach(ARENA_TARGET, worklog_path)
        metrics["orchestrator_overreach_detected"] = overreach[
            "orchestrator_overreach_detected"
        ]
        metrics["overreach_evidence"] = overreach["overreach_evidence"]
        metrics["overreach_severity"] = overreach["severity"]

        # Apply strict mode: upgrade any overreach to critical
        if args.strict and overreach["orchestrator_overreach_detected"]:
            overreach["severity"] = "critical"
            metrics["overreach_severity"] = "critical"

        if overreach["severity"] == "critical":
            logger.error(
                f"Orchestrator overreach detected for {model} — "
                f"severity=CRITICAL. Marking result as INVALID. "
                f"Evidence: {overreach['overreach_evidence']}"
            )
            metrics["status"] = "invalid"
        elif overreach["severity"] == "warning":
            logger.warning(
                f"Orchestrator overreach detected for {model} — "
                f"severity=WARNING. Result still marked as completed. "
                f"Evidence: {overreach['overreach_evidence']}"
            )
            _record_completed(metrics)
        else:
            _record_completed(metrics)

        # 6. Save metrics
        save_metrics(model, metrics)

        # 7. Archive results
        archive_results(model)

    # Compile final results
    compile_final_results()
    logger.info("Arena benchmark complete")


if __name__ == "__main__":
    main()
