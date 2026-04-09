"""
Arena Telemetry Parser

Analyzes project artifacts after a benchmark run:
- Parses WORKLOG.md for QA rejection/approval counts
- Calculates Time-to-Done-Done from timestamps
- Runs Go static analysis tools (go test, golangci-lint, gosec, govulncheck)
- Verifies COMPLETION_REPORT.md exists and contains approval
- Outputs a JSON metrics object to stdout
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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
# Constants
# ---------------------------------------------------------------------------

TIMESTAMP_RE = re.compile(
    r"^\[?(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\]?"
)
REVIEW_REJECTED_RE = re.compile(r"REVIEW_REJECTED", re.IGNORECASE)
REVIEW_APPROVED_RE = re.compile(r"REVIEW_APPROVED", re.IGNORECASE)
COMPLETION_RE = re.compile(
    r"(?:PROJECT_COMPLETED|COMPLETION_REPORT)", re.IGNORECASE
)

# ---------------------------------------------------------------------------
# WORKLOG parsing
# ---------------------------------------------------------------------------


def parse_worklog(project_dir: Path) -> dict[str, Any]:
    """Parse WORKLOG.md for QA rejections, approvals, and timing.

    Returns a dict with qa_rejections, qa_approvals, time_to_done_seconds,
    and golden_task_completed (based on finding a completion marker).
    """
    worklog_path = project_dir / "WORKLOG.md"
    if not worklog_path.exists():
        logger.warning(f"No WORKLOG.md found in {project_dir}")
        return {
            "qa_rejections": -1,
            "qa_approvals": -1,
            "time_to_done_seconds": -1,
            "golden_task_completed": False,
        }

    lines = worklog_path.read_text().splitlines()
    qa_rejections = 0
    qa_approvals = 0
    first_ts: datetime | None = None
    completion_ts: datetime | None = None
    golden_completed = False

    for line in lines:
        # Count QA decisions
        if REVIEW_REJECTED_RE.search(line):
            qa_rejections += 1
        if REVIEW_APPROVED_RE.search(line):
            qa_approvals += 1

        # Track completion
        if COMPLETION_RE.search(line):
            golden_completed = True
            m = TIMESTAMP_RE.match(line)
            if m:
                completion_ts = _parse_ts(m.group(1))

        # Capture first timestamp
        if first_ts is None:
            m = TIMESTAMP_RE.match(line)
            if m:
                first_ts = _parse_ts(m.group(1))

    time_to_done = -1
    if first_ts and completion_ts:
        delta = (completion_ts - first_ts).total_seconds()
        time_to_done = max(0, int(delta))
    elif first_ts and golden_completed:
        # Completion marker found but no parseable completion timestamp —
        # fall back to "same second" (effectively instant from log perspective)
        time_to_done = 0

    return {
        "qa_rejections": qa_rejections,
        "qa_approvals": qa_approvals,
        "time_to_done_seconds": time_to_done,
        "golden_task_completed": golden_completed,
    }


def _parse_ts(ts_str: str) -> datetime:
    """Parse a timestamp string like '2026-04-09 04:30' into a datetime."""
    return datetime.strptime(ts_str.strip(), "%Y-%m-%d %H:%M").replace(
        tzinfo=timezone.utc
    )


# ---------------------------------------------------------------------------
# Go static analysis
# ---------------------------------------------------------------------------


def _run_cmd(args: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """Run a subprocess and return (returncode, stdout, stderr).

    If *cwd* is provided it is passed to ``subprocess.run`` so that
    tools like ``go test`` execute in the correct project directory.
    """
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=cwd,
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        logger.warning(f"Command not found: {args[0]}")
        return -1, "", "unavailable"
    except subprocess.TimeoutExpired:
        logger.warning(f"Command timed out: {args[0]}")
        return -1, "", "timeout"


def get_test_coverage(project_dir: Path) -> float:
    """Run `go test -cover ./...` and extract the coverage percentage.

    Returns -1 if the tool is unavailable or parsing fails.
    """
    rc, stdout, stderr = _run_cmd(
        ["go", "test", "-cover", "./..."],
        cwd=project_dir,
    )
    if rc == -1:
        return -1

    # Look for lines like "ok\tgithub.com/...\t0.123s\tcoverage: 87.5% of statements"
    # or the summary line "coverage: 87.5% of statements"
    for line in (stdout + stderr).splitlines():
        m = re.search(r"coverage:\s+([\d.]+)%", line)
        if m:
            return float(m.group(1))

    # If tests ran but no coverage output, check if tests passed
    if rc == 0:
        logger.warning("go test passed but no coverage percentage found")
        return 0.0

    logger.warning(f"go test failed (rc={rc}): {stderr}")
    return -1


def count_lint_warnings(project_dir: Path) -> int:
    """Run `golangci-lint run ./...` and count warning lines.

    Returns -1 if unavailable.
    """
    rc, stdout, stderr = _run_cmd(
        ["golangci-lint", "run", "./..."],
        cwd=project_dir,
    )
    if rc == -1:
        return -1

    # Each warning is typically one line
    lines = [line for line in (stdout + stderr).splitlines() if line.strip()]
    return len(lines)


def count_gosec_issues(project_dir: Path) -> int:
    """Run `gosec ./...` and count issues found.

    Returns -1 if unavailable.
    """
    rc, stdout, stderr = _run_cmd(
        ["gosec", "./..."],
        cwd=project_dir,
    )
    if rc == -1:
        return -1

    # gosec outputs a summary line like "Results:\n\nGolang errors: 0"
    # and lists issues. Count non-empty lines that look like issue entries.
    # The summary typically has "[failures: N]" or we count lines between
    # header and summary.
    output = stdout + stderr
    m = re.search(r"\[failures:\s*(\d+)\]", output, re.IGNORECASE)
    if m:
        return int(m.group(1))

    # Fallback: count lines containing "Golang errors" or issue markers
    issue_lines = [
        line for line in output.splitlines()
        if re.search(r"\b(G4\d\d|G3\d\d|G2\d\d|G1\d\d)\b", line)
    ]
    return len(issue_lines)


def count_govulncheck_issues(project_dir: Path) -> int:
    """Run `govulncheck ./...` and count applicable vulnerabilities.

    Returns -1 if unavailable.
    """
    rc, stdout, stderr = _run_cmd(
        ["govulncheck", "./..."],
        cwd=project_dir,
    )
    if rc == -1:
        return -1

    output = stdout + stderr
    # govulncheck outputs lines like "Vuln ID: GHSA-..."
    vuln_lines = [
        line for line in output.splitlines()
        if re.search(r"Vuln ID|GHSA-", line, re.IGNORECASE)
    ]
    return len(vuln_lines)


# ---------------------------------------------------------------------------
# Completion check
# ---------------------------------------------------------------------------


def check_completion(project_dir: Path) -> bool:
    """Verify COMPLETION_REPORT.md exists and contains an approval indicator.

    Returns True if the task was approved/completed.
    """
    report = project_dir / "COMPLETION_REPORT.md"
    if not report.exists():
        logger.warning("No COMPLETION_REPORT.md found")
        return False

    content = report.read_text().lower()
    # Look for positive completion signals
    positive_signals = [
        "approved",
        "completed",
        "done",
        "✅",
        "pass",
    ]
    return any(signal in content for signal in positive_signals)


# ---------------------------------------------------------------------------
# Orchestrator overreach detection
# ---------------------------------------------------------------------------

# Patterns that suggest the orchestrator wrote implementation code
# (applied to WORKLOG entries attributed to pm_bot / orchestrator)
_IMPLEMENTATION_PATTERNS = [
    re.compile(r"\b(implemented|implementing|implementation)\b", re.IGNORECASE),
    re.compile(r"\b(wrote|written|writing)\b\s+.*\b(code|file|function|method|package|struct|interface|test)\b", re.IGNORECASE),
    re.compile(r"\bcreated\b\s+.*\b(file|package|module|struct|function|method|test|\.(go|sh|mod|sum))\b", re.IGNORECASE),
    re.compile(r"\b(fixed|fixing|fix)\b\s+.*\b(code|bug|issue|error|failing test|build|compilation|lint)\b", re.IGNORECASE),
    re.compile(r"\b(built|building|build|compiled|compiling)\b", re.IGNORECASE),
    re.compile(r"\b(let me try to build|let me implement|I will implement|I'll implement|I will write|I'll write)\b", re.IGNORECASE),
]

# Subagent identifiers — entries from these are expected to do implementation
_SUBAGENT_IDS = {"dev_bot", "py_bot", "qa_bot"}

# Keywords that indicate a spawn/launch of a subagent in a WORKLOG entry
_SPAWN_PATTERNS = [
    re.compile(r"\b(spawn|spawning|spawned|launch|launched|started)\b.*\bdev_bot\b", re.IGNORECASE),
]


def detect_orchestrator_overreach(
    project_dir: Path,
    worklog_path: Path | None = None,
) -> dict[str, Any]:
    """Detect when the orchestrator (pm_bot) wrote implementation code itself.

    This is a post-run check: if the orchestrator ignored instructions and
    implemented code instead of just orchestrating, the benchmark data for
    that run is untrustworthy.

    Detection signals:
      1. WORKLOG entries from the orchestrator that mention implementation
         activities (writing code, building, fixing compilation, etc.)
      2. Code files (.go, go.mod, Makefile, etc.) created without a
         corresponding dev_bot spawn entry in the WORKLOG
      3. COMPLETION_REPORT.md present but no dev_bot activity in WORKLOG

    Args:
        project_dir: The arena-target/ directory from a benchmark run.
        worklog_path: Override path to WORKLOG.md. If None, uses
            project_dir / "WORKLOG.md".

    Returns:
        A dict with:
            orchestrator_overreach_detected: bool
            overreach_evidence: list[str] — human-readable descriptions
            severity: "none" | "warning" | "critical"
    """
    if worklog_path is None:
        worklog_path = project_dir / "WORKLOG.md"

    evidence: list[str] = []

    # --- Signal 1: Orchestrator WORKLOG entries mentioning implementation ---
    if worklog_path.exists():
        lines = worklog_path.read_text().splitlines()
        dev_bot_spawned = False
        dev_bot_completed = False

        for line in lines:
            # Check if dev_bot was spawned
            for pat in _SPAWN_PATTERNS:
                if pat.search(line):
                    dev_bot_spawned = True

            # Check if dev_bot completed work (not just started)
            if re.search(r"\bdev_bot\b", line, re.IGNORECASE) and re.search(
                r"\b(complete|completed|done|finished)\b", line, re.IGNORECASE
            ):
                dev_bot_completed = True

            # Parse the agent field from WORKLOG format:
            # "YYYY-MM-DD HH:MM | AGENT | ACTION | DESCRIPTION"
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                agent = parts[1].strip().lower()
                full_text = line

                # Only flag entries NOT from dev_bot/py_bot (they're supposed
                # to implement)
                if agent not in {s.lower() for s in _SUBAGENT_IDS}:
                    for pat in _IMPLEMENTATION_PATTERNS:
                        if pat.search(full_text):
                            evidence.append(
                                f"Orchestrator entry suggests implementation: "
                                f"{line.strip()}"
                            )
                            break

        # --- Signal 2: Code files without dev_bot spawn ---
        code_extensions = {".go"}
        code_basenames = {"go.mod", "go.sum", "Makefile", "makefile"}
        code_files_found = False

        for item in project_dir.rglob("*"):
            if item.is_file():
                if item.suffix in code_extensions or item.name in code_basenames:
                    # Skip files that are part of the test harness itself
                    # (e.g., in a parent directory)
                    code_files_found = True
                    break

        if code_files_found and not dev_bot_spawned:
            evidence.append(
                "Code files found in project but no dev_bot spawn entry in "
                "WORKLOG — orchestrator may have written code directly"
            )

        # --- Signal 3: COMPLETION_REPORT without dev_bot completion ---
        completion_report = project_dir / "COMPLETION_REPORT.md"
        if completion_report.exists() and not dev_bot_completed and not dev_bot_spawned:
            evidence.append(
                "COMPLETION_REPORT.md exists but no dev_bot spawn or "
                "completion in WORKLOG — orchestrator may have done the work"
            )
    else:
        # No WORKLOG at all but code files exist — very suspicious
        code_extensions = {".go"}
        code_basenames = {"go.mod", "go.sum", "Makefile", "makefile"}
        for item in project_dir.rglob("*"):
            if item.is_file():
                if item.suffix in code_extensions or item.name in code_basenames:
                    evidence.append(
                        "Code files found but no WORKLOG.md — "
                        "cannot verify subagent involvement"
                    )
                    break

    # --- Determine severity ---
    if not evidence:
        severity = "none"
    elif len(evidence) == 1:
        severity = "warning"
    else:
        # Multiple signals = critical
        severity = "critical"

    return {
        "orchestrator_overreach_detected": len(evidence) > 0,
        "overreach_evidence": evidence,
        "severity": severity,
    }


# ---------------------------------------------------------------------------
# CLI & main
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Arena Telemetry Parser — analyze benchmark run artifacts",
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        required=True,
        help="Path to the project directory (arena-target/ after a run)",
    )
    parser.add_argument(
        "--model",
        help="Model identifier to include in output (optional if not provided, "
        "will try to read from arena_config.json)",
    )
    return parser


def resolve_model(project_dir: Path, explicit: str | None) -> str:
    if explicit:
        return explicit

    # Try to read from arena_config.json in the parent directory
    config_path = project_dir.parent / "arena_config.json"
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text())
            return data.get("model", "unknown")
        except (json.JSONDecodeError, OSError):
            pass

    return "unknown"


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    project_dir = args.project_dir.resolve()
    if not project_dir.exists():
        logger.error(f"Project directory does not exist: {project_dir}")
        sys.exit(1)

    model = resolve_model(project_dir, args.model)

    # 1. Parse WORKLOG.md
    worklog_metrics = parse_worklog(project_dir)

    # 2. Run Go static analysis
    coverage = get_test_coverage(project_dir)
    lint_warnings = count_lint_warnings(project_dir)
    gosec_issues = count_gosec_issues(project_dir)
    vulncheck_issues = count_govulncheck_issues(project_dir)

    # 3. Check completion
    golden_completed = check_completion(project_dir)
    # Override with WORKLOG-based detection if COMPLETION_REPORT check failed
    if not golden_completed and worklog_metrics["golden_task_completed"]:
        golden_completed = True

    metrics: dict[str, Any] = {
        "model": model,
        "qa_rejections": worklog_metrics["qa_rejections"],
        "qa_approvals": worklog_metrics["qa_approvals"],
        "time_to_done_seconds": worklog_metrics["time_to_done_seconds"],
        "test_coverage_percent": coverage,
        "lint_warnings": lint_warnings,
        "gosec_issues": gosec_issues,
        "govulncheck_issues": vulncheck_issues,
        "golden_task_completed": golden_completed,
    }

    # Output JSON to stdout (for benchmark_runner to capture)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
