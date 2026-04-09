# Arena — LLM Benchmarking Harness

Arena is a benchmarking harness for evaluating LLM models against a standardized Golden Task (a weather-cache CLI tool built with wttr.in + SQLite). It orchestrates model runs, collects telemetry via Go static-analysis tools, and posts completion webhooks.

## Dependencies

```bash
pip install requests
```

The telemetry scripts also invoke these Go tools (must be on `$PATH`):

- `go` (for `go test -cover`)
- `golangci-lint`
- `gosec`
- `govulncheck`

## Project Structure

```
arena/
  benchmark_runner.py   # Orchestrator: launches models, polls for results, calls webhooks
  telemetry.py          # Metrics: parses WORKLOG, runs Go tools, emits JSON metrics
  tests/
    test_arena.py       # 38 tests covering both modules
  GOLDEN_TASK.md        # The standardized task all models implement
  EVALUATION_PROMPT.md  # Rubric for the judge (pm_bot)
  PYTHON_STANDARDS.md   # Team coding conventions
  WORKFLOW.md           # End-to-end workflow description
  HANDOVER_PROTOCOL.md  # Handover / sign-off rules
  WORKLOG.md            # Running log of all project events
```

## CLI Usage

### benchmark_runner.py

Main orchestrator. Reads `arena_config.json` for the list of models, creates a clean target directory per model, runs the benchmark, collects telemetry, and fires a webhook to trigger an autonomous agent run.

```bash
python3 benchmark_runner.py \
    --models "openrouter/kwaipilot/kat-coder-pro-v2" "openrouter/xiaomi/mimo-v2-flash" \
    --hook-token YOUR_TOKEN
```

**Or use a config file:**

```bash
python3 benchmark_runner.py \
    --config arena_config.json \
    --hook-token YOUR_TOKEN
```

**Arguments:**

| Flag | Required | Description |
|------|----------|-------------|
| `--models` | Yes* | Space-separated model identifiers to benchmark |
| `--config` | Yes* | Path to JSON file with a `models` key listing model identifiers |
| `--hook-token` | Yes | Bearer token for the OpenClaw `/hooks/agent` endpoint |
| `--gateway-url` | No | OpenClaw gateway URL (default: `http://127.0.0.1:18789`) |
| `--timeout` | No | Per-model timeout in seconds (default: 1800) |
| `--skip-preflight` | No | Skip prerequisite checks (useful for testing) |
| `--fail-fast` | No | Stop the entire benchmark suite if any model fails (default: continue) |
| `--retry` | No | Retry failed models up to N times (default: 0) |
| `--strict` | No | Treat ANY orchestrator overreach as critical (default: warning for minor, critical for obvious) |

*One of `--models` or `--config` is required.

### telemetry.py

Analyzes a single model's run artifacts and prints a JSON metrics object to stdout.

```bash
python3 telemetry.py \
    --project-dir arena-target/model-gpt4 \
    --model gpt-4
```

**Arguments:**

| Flag | Required | Description |
|------|----------|-------------|
| `--project-dir` | Yes | Path to the model's target directory |
| `--model` | No | Model identifier (falls back to `arena_config.json` or `"unknown"`) |

**Metrics collected:**

- `qa_rejections` / `qa_approvals` — parsed from WORKLOG.md
- `time_to_done_seconds` — elapsed time from first log entry to completion
- `test_coverage_percent` — from `go test -cover`
- `lint_warnings` — count of `golangci-lint` findings
- `gosec_issues` — count of security findings
- `govulncheck_issues` — count of vulnerability findings
- `golden_task_completed` — whether COMPLETION_REPORT.md signals approval

## Example Invocations

**Run the full benchmark suite:**

```bash
python3 benchmark_runner.py \
    --config arena_config.json \
    --output-dir arena-target \
    --webhook-url https://hooks.internal/arena \
    --webhook-token "$(vault read -field=token secret/arena)"
```

**Telemetry for a single model:**

```bash
python3 telemetry.py --project-dir arena-target/model-gpt4 --model gpt-4 > metrics.json
```

**Run the test suite:**

```bash
python3 -m pytest tests/ -v
```

## Webhook Integration

`benchmark_runner.py` uses the OpenClaw `/hooks/agent` endpoint to trigger autonomous benchmark runs. For each model, it POSTs a comprehensive prompt to the isolated agent endpoint, which then orchestrates the full workflow (spawn dev_bot → qa_bot → iterate → complete) without depending on any existing session or heartbeat.

**Endpoint:** `POST {gateway_url}/hooks/agent`

**Headers:**
- `Authorization: Bearer <hook-token>`
- `Content-Type: application/json`
- `x-openclaw-model: <model>`

**Payload:**
```json
{
  "message": "<self-contained prompt instructing the agent to act as pm_bot>",
  "name": "arena-benchmark"
}
```

The token is sent as an `Authorization: Bearer <token>` header. The token is **never** logged or written to disk — it arrives only via CLI arguments.

### Preflight Checks

Before starting any runs, `benchmark_runner.py` performs prerequisite checks:
1. **Go is installed** — verifies `go version` exits 0
2. **Gateway is reachable** — verifies `GET /v1/models` returns 200 or 401
3. **Config directory is writable** — verifies `arena_config.json` parent directory accepts writes

Use `--skip-preflight` to bypass these checks (useful for testing).

### Failure Handling

When a spawned model fails or times out, the runner records the outcome:
- **FAILED.md** — If the isolated agent detects a subagent failure, it writes `FAILED.md` instead of attempting the work itself. The runner parses this and records `status: failed`.
- **Timeout** — If neither `COMPLETION_REPORT.md` nor `FAILED.md` appears within the timeout, the run is recorded as `status: timeout`.
- **`FINAL_RESULTS.json`** — Every model entry now includes a `status` field: `completed`, `failed`, `timeout`, or `unknown`.

Use `--fail-fast` to abort the suite on the first failure. Use `--retry N` to retry failed models up to N times.

### Orchestrator Overreach Detection

The benchmark measures the **spawned model's** coding ability — not the orchestrator's. If the orchestrator (pm_bot) ignores instructions and implements code itself when a subagent fails, the benchmark data is invalid.

To prevent this, the harness has two layers of protection:

1. **Strengthened prompt** — The prohibition against implementing code is stated in three distinct sections of the agent prompt (opening, workflow reminder, failure handling), using the strongest possible language ("CRITICAL RULE", "ABSOLUTELY FORBIDDEN", "UNDER NO CIRCUMSTANCES").

2. **Telemetry detection** — After a "completed" run, `telemetry.detect_orchestrator_overreach()` scans the WORKLOG and project files for signs the orchestrator wrote code:
   - WORKLOG entries from pm_bot mentioning implementation activities (writing code, building, fixing compilation)
   - Code files (.go, go.mod, Makefile) present without a corresponding dev_bot spawn entry
   - COMPLETION_REPORT.md written without any dev_bot activity

**Severity levels:**
- `none` — No overreach detected; result marked `status: "completed"`
- `warning` — One weak signal; result stays `completed` but evidence is recorded
- `critical` — Multiple signals or clear evidence; result marked `status: "invalid"`

Use `--strict` to treat ANY overreach signal as critical.

**FINAL_RESULTS.json fields:**
```json
{
  "model": "...",
  "status": "completed|failed|timeout|invalid",
  "orchestrator_overreach_detected": false,
  "overreach_evidence": [],
  "overreach_severity": "none|warning|critical"
}
```

## Development

```bash
# Run tests
python3 -m pytest tests/ -v

# Lint
flake8 benchmark_runner.py telemetry.py
```

All code follows the conventions in `PYTHON_STANDARDS.md`: type hints, `pathlib`, `argparse`, no `shell=True`, and `from __future__ import annotations`.
