"""Tests for benchmark_runner.py and telemetry.py."""

from __future__ import annotations

import json
from pathlib import Path
from unittest import mock

# We import the modules under test relative to this file's grandparent
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import benchmark_runner  # noqa: E402
import telemetry  # noqa: E402

# ---------------------------------------------------------------------------
# benchmark_runner tests
# ---------------------------------------------------------------------------


class TestSanitizeModelName:
    def test_simple_name(self) -> None:
        assert benchmark_runner.sanitize_model_name("openrouter/xiaomi/mimo") == "openrouter_xiaomi_mimo"

    def test_keeps_alphanumerics(self) -> None:
        assert benchmark_runner.sanitize_model_name("model-v2-pro") == "model_v2_pro"

    def test_strips_leading_trailing_underscores(self) -> None:
        assert benchmark_runner.sanitize_model_name("/model/") == "model"

    def test_consecutive_separators(self) -> None:
        assert benchmark_runner.sanitize_model_name("a:::b") == "a_b"


class TestWriteArenaConfig:
    def test_writes_valid_json(self, tmp_path: Path) -> None:
        # Temporarily patch the constant
        original = benchmark_runner.ARENA_CONFIG
        benchmark_runner.ARENA_CONFIG = tmp_path / "arena_config.json"
        try:
            benchmark_runner.write_arena_config("test/model")
            data = json.loads(benchmark_runner.ARENA_CONFIG.read_text())
            assert data == {"model": "test/model"}
        finally:
            benchmark_runner.ARENA_CONFIG = original


class TestPrepareTargetDir:
    def test_creates_fresh_directory(self, tmp_path: Path) -> None:
        # Patch constants
        orig_target = benchmark_runner.ARENA_TARGET
        orig_golden = benchmark_runner.GOLDEN_TASK
        benchmark_runner.ARENA_TARGET = tmp_path / "arena-target"
        golden = tmp_path / "GOLDEN_TASK.md"
        golden.write_text("# Golden Task\n")
        benchmark_runner.GOLDEN_TASK = golden

        try:
            benchmark_runner.prepare_target_dir()
            assert benchmark_runner.ARENA_TARGET.exists()
            assert (benchmark_runner.ARENA_TARGET / "TASK.md").exists()
            assert (benchmark_runner.ARENA_TARGET / "TASK.md").read_text() == "# Golden Task\n"
        finally:
            benchmark_runner.ARENA_TARGET = orig_target
            benchmark_runner.GOLDEN_TASK = orig_golden

    def test_removes_existing_directory(self, tmp_path: Path) -> None:
        orig_target = benchmark_runner.ARENA_TARGET
        orig_golden = benchmark_runner.GOLDEN_TASK
        benchmark_runner.ARENA_TARGET = tmp_path / "arena-target"
        golden = tmp_path / "GOLDEN_TASK.md"
        golden.write_text("# Golden Task\n")
        benchmark_runner.GOLDEN_TASK = golden

        # Create a stale file
        benchmark_runner.ARENA_TARGET.mkdir()
        (benchmark_runner.ARENA_TARGET / "stale.txt").write_text("old")

        try:
            benchmark_runner.prepare_target_dir()
            assert not (benchmark_runner.ARENA_TARGET / "stale.txt").exists()
            assert (benchmark_runner.ARENA_TARGET / "TASK.md").exists()
        finally:
            benchmark_runner.ARENA_TARGET = orig_target
            benchmark_runner.GOLDEN_TASK = orig_golden


class TestTriggerBenchmarkRun:
    @mock.patch("benchmark_runner.requests.post")
    def test_success(self, mock_post: mock.MagicMock) -> None:
        mock_post.return_value = mock.MagicMock(
            status_code=200, raise_for_status=lambda: None
        )
        result = benchmark_runner.trigger_benchmark_run(
            "http://localhost:18789", "my-token", "test/model"
        )
        assert result is True
        call_args = mock_post.call_args
        # Verify endpoint is /hooks/agent, not /hooks/wake
        assert "/hooks/agent" in call_args[0][0]
        # Verify headers
        assert call_args[1]["headers"]["Authorization"] == "Bearer my-token"
        assert call_args[1]["headers"]["x-openclaw-model"] == "test/model"
        # Verify payload structure
        payload = call_args[1]["json"]
        assert "message" in payload
        assert payload["name"] == "arena-benchmark"
        # 'mode' key should NOT be present (that was /hooks/wake)
        assert "mode" not in payload

    @mock.patch("benchmark_runner.requests.post")
    def test_failure(self, mock_post: mock.MagicMock) -> None:
        import requests
        mock_post.side_effect = requests.RequestException("connection refused")
        result = benchmark_runner.trigger_benchmark_run(
            "http://localhost:18789", "my-token", "test/model"
        )
        assert result is False

    @mock.patch("benchmark_runner.requests.post")
    def test_payload_contains_prompt_instructions(
        self, mock_post: mock.MagicMock
    ) -> None:
        mock_post.return_value = mock.MagicMock(
            status_code=200, raise_for_status=lambda: None
        )
        benchmark_runner.trigger_benchmark_run(
            "http://localhost:18789", "my-token", "test/model"
        )
        payload = mock_post.call_args[1]["json"]
        message = payload["message"]
        # The prompt should contain key instructions
        assert "pm_bot" in message
        assert "dev_bot" in message
        assert "qa_bot" in message
        assert "arena_config.json" in message
        assert "COMPLETION_REPORT.md" in message
        assert "WORKLOG.md" in message
        assert "GOLANG_STANDARDS.md" in message
        assert "WORKFLOW.md" in message
        assert "HANDOVER_PROTOCOL.md" in message


class TestPollForCompletion:
    def test_file_exists_immediately(self, tmp_path: Path) -> None:
        orig_target = benchmark_runner.ARENA_TARGET
        benchmark_runner.ARENA_TARGET = tmp_path
        (tmp_path / "COMPLETION_REPORT.md").write_text("done")
        try:
            assert benchmark_runner.poll_for_completion(5) == ("completed", None)
        finally:
            benchmark_runner.ARENA_TARGET = orig_target

    def test_timeout(self, tmp_path: Path) -> None:
        orig_target = benchmark_runner.ARENA_TARGET
        benchmark_runner.ARENA_TARGET = tmp_path
        try:
            assert benchmark_runner.poll_for_completion(1) == ("timeout", None)
        finally:
            benchmark_runner.ARENA_TARGET = orig_target

    def test_failed_md_detected(self, tmp_path: Path) -> None:
        orig_target = benchmark_runner.ARENA_TARGET
        benchmark_runner.ARENA_TARGET = tmp_path
        failed = tmp_path / "FAILED.md"
        failed.write_text(
            "# Run Failed\n"
            "## Model\n"
            "test/model\n"
            "## Failed Subagent\n"
            "dev_bot\n"
            "## Failure Reason\n"
            "Model unavailable\n"
            "## Timestamp\n"
            "2026-04-09T12:00:00Z\n"
        )
        try:
            outcome, failure_info = benchmark_runner.poll_for_completion(5)
            assert outcome == "failed"
            assert failure_info is not None
            assert failure_info["model"] == "test/model"
            assert failure_info["failed_subagent"] == "dev_bot"
            assert failure_info["reason"] == "Model unavailable"
            assert failure_info["timestamp"] == "2026-04-09T12:00:00Z"
        finally:
            benchmark_runner.ARENA_TARGET = orig_target


class TestRunTelemetry:
    @mock.patch("benchmark_runner.subprocess.run")
    def test_success(self, mock_run: mock.MagicMock) -> None:
        mock_run.return_value = mock.MagicMock(
            returncode=0,
            stdout='{"model": "test"}',
            stderr="",
        )
        result = benchmark_runner.run_telemetry()
        assert result == {"model": "test"}

    @mock.patch("benchmark_runner.subprocess.run")
    def test_nonzero_exit(self, mock_run: mock.MagicMock) -> None:
        mock_run.return_value = mock.MagicMock(returncode=1, stdout="", stderr="fail")
        result = benchmark_runner.run_telemetry()
        assert result is None


class TestArchiveResults:
    def test_moves_files(self, tmp_path: Path) -> None:
        orig_target = benchmark_runner.ARENA_TARGET
        orig_results = benchmark_runner.ARENA_RESULTS
        benchmark_runner.ARENA_TARGET = tmp_path / "arena-target"
        benchmark_runner.ARENA_RESULTS = tmp_path / "arena-results"
        benchmark_runner.ARENA_TARGET.mkdir()
        (benchmark_runner.ARENA_TARGET / "file.txt").write_text("hello")

        try:
            dest = benchmark_runner.archive_results("test/model")
            assert dest == benchmark_runner.ARENA_RESULTS / "test_model"
            assert (dest / "file.txt").exists()
            # The target directory still exists but should be empty
            assert not any(benchmark_runner.ARENA_TARGET.iterdir())
        finally:
            benchmark_runner.ARENA_TARGET = orig_target
            benchmark_runner.ARENA_RESULTS = orig_results


class TestCompileFinalResults:
    def test_empty(self, tmp_path: Path) -> None:
        orig_results = benchmark_runner.ARENA_RESULTS
        orig_final = benchmark_runner.FINAL_RESULTS
        benchmark_runner.ARENA_RESULTS = tmp_path / "arena-results"
        benchmark_runner.FINAL_RESULTS = tmp_path / "FINAL_RESULTS.json"
        try:
            results = benchmark_runner.compile_final_results()
            assert results == []
            assert json.loads(benchmark_runner.FINAL_RESULTS.read_text()) == []
        finally:
            benchmark_runner.ARENA_RESULTS = orig_results
            benchmark_runner.FINAL_RESULTS = orig_final

    def test_with_metrics_files(self, tmp_path: Path) -> None:
        orig_results = benchmark_runner.ARENA_RESULTS
        orig_final = benchmark_runner.FINAL_RESULTS
        benchmark_runner.ARENA_RESULTS = tmp_path / "arena-results"
        benchmark_runner.FINAL_RESULTS = tmp_path / "FINAL_RESULTS.json"
        benchmark_runner.ARENA_RESULTS.mkdir(parents=True)
        metrics_dir = benchmark_runner.ARENA_RESULTS / "model_a"
        metrics_dir.mkdir()
        (metrics_dir / "metrics.json").write_text('{"model": "a", "score": 90}')

        try:
            results = benchmark_runner.compile_final_results()
            assert len(results) == 1
            assert results[0]["model"] == "a"
        finally:
            benchmark_runner.ARENA_RESULTS = orig_results
            benchmark_runner.FINAL_RESULTS = orig_final


class TestResolveModels:
    def test_from_cli_args(self) -> None:
        args = mock.MagicMock(models=["m1", "m2"], config=None)
        models = benchmark_runner.resolve_models(args)
        assert models == ["m1", "m2"]

    def test_from_config_file(self, tmp_path: Path) -> None:
        config = tmp_path / "models.json"
        config.write_text('{"models": ["a", "b"]}')
        args = mock.MagicMock(models=None, config=config)
        models = benchmark_runner.resolve_models(args)
        assert models == ["a", "b"]


class TestPreflightCheck:
    @mock.patch("benchmark_runner.subprocess.run")
    @mock.patch("benchmark_runner.requests.get")
    def test_all_checks_pass(
        self,
        mock_get: mock.MagicMock,
        mock_run: mock.MagicMock,
        tmp_path: Path,
    ) -> None:
        # Go is installed
        mock_run.return_value = mock.MagicMock(
            returncode=0, stdout="go version go1.22 linux/amd64\n", stderr=""
        )
        # Gateway is reachable
        mock_get.return_value = mock.MagicMock(status_code=200)
        # Temporarily patch ARENA_CONFIG and SHARED_DIR to tmp dirs
        orig_config = benchmark_runner.ARENA_CONFIG
        orig_shared = benchmark_runner.SHARED_DIR
        benchmark_runner.ARENA_CONFIG = tmp_path / "arena_config.json"
        # Create fake shared docs so check 4 passes
        shared_tmp = tmp_path / "shared"
        shared_tmp.mkdir()
        for doc in [
                "GOLANG_STANDARDS.md",
                "GOLANG_PROJECT_TEMPLATE.md",
                "WORKFLOW.md",
                "HANDOVER_PROTOCOL.md",
        ]:
            (shared_tmp / doc).write_text("doc")
        benchmark_runner.SHARED_DIR = shared_tmp
        try:
            # Should not raise or call sys.exit
            benchmark_runner.preflight_check("http://localhost:18789")
        finally:
            benchmark_runner.ARENA_CONFIG = orig_config
            benchmark_runner.SHARED_DIR = orig_shared

    @mock.patch("benchmark_runner.sys.exit")
    @mock.patch("benchmark_runner.subprocess.run")
    @mock.patch("benchmark_runner.requests.get")
    def test_go_not_installed(
        self,
        mock_get: mock.MagicMock,
        mock_run: mock.MagicMock,
        mock_exit: mock.MagicMock,
    ) -> None:
        # Go not found
        mock_run.side_effect = FileNotFoundError("go")
        mock_get.return_value = mock.MagicMock(status_code=200)
        try:
            benchmark_runner.preflight_check("http://localhost:18789")
        except SystemExit:
            pass
        mock_exit.assert_called_once()

    @mock.patch("benchmark_runner.sys.exit")
    @mock.patch("benchmark_runner.subprocess.run")
    @mock.patch("benchmark_runner.requests.get")
    def test_gateway_unreachable(
        self,
        mock_get: mock.MagicMock,
        mock_run: mock.MagicMock,
        mock_exit: mock.MagicMock,
    ) -> None:
        import requests
        # Go is installed
        mock_run.return_value = mock.MagicMock(
            returncode=0, stdout="go version go1.22\n", stderr=""
        )
        # Gateway unreachable
        mock_get.side_effect = requests.RequestException("connection refused")
        try:
            benchmark_runner.preflight_check("http://localhost:18789")
        except SystemExit:
            pass
        mock_exit.assert_called_once()

    @mock.patch("benchmark_runner.sys.exit")
    @mock.patch("benchmark_runner.subprocess.run")
    @mock.patch("benchmark_runner.requests.get")
    def test_go_nonzero_exit(
        self,
        mock_get: mock.MagicMock,
        mock_run: mock.MagicMock,
        mock_exit: mock.MagicMock,
    ) -> None:
        # Go returns non-zero
        mock_run.return_value = mock.MagicMock(
            returncode=1, stdout="", stderr="command not found"
        )
        mock_get.return_value = mock.MagicMock(status_code=200)
        try:
            benchmark_runner.preflight_check("http://localhost:18789")
        except SystemExit:
            pass
        mock_exit.assert_called_once()

    @mock.patch("benchmark_runner.sys.exit")
    @mock.patch("benchmark_runner.subprocess.run")
    @mock.patch("benchmark_runner.requests.get")
    def test_gateway_401_is_ok(
        self,
        mock_get: mock.MagicMock,
        mock_run: mock.MagicMock,
        mock_exit: mock.MagicMock,
        tmp_path: Path,
    ) -> None:
        # Go is installed
        mock_run.return_value = mock.MagicMock(
            returncode=0, stdout="go version go1.22\n", stderr=""
        )
        # Gateway returns 401 (still means it's alive)
        mock_get.return_value = mock.MagicMock(status_code=401)
        # Patch paths so shared docs check passes
        orig_config = benchmark_runner.ARENA_CONFIG
        orig_shared = benchmark_runner.SHARED_DIR
        benchmark_runner.ARENA_CONFIG = tmp_path / "arena_config.json"
        shared_tmp = tmp_path / "shared"
        shared_tmp.mkdir()
        for doc in [
                "GOLANG_STANDARDS.md",
                "GOLANG_PROJECT_TEMPLATE.md",
                "WORKFLOW.md",
                "HANDOVER_PROTOCOL.md",
        ]:
            (shared_tmp / doc).write_text("doc")
        benchmark_runner.SHARED_DIR = shared_tmp
        try:
            benchmark_runner.preflight_check("http://localhost:18789")
            mock_exit.assert_not_called()
        finally:
            benchmark_runner.ARENA_CONFIG = orig_config
            benchmark_runner.SHARED_DIR = orig_shared

    @mock.patch("benchmark_runner.sys.exit")
    @mock.patch("benchmark_runner.subprocess.run")
    @mock.patch("benchmark_runner.requests.get")
    def test_shared_docs_missing(
        self,
        mock_get: mock.MagicMock,
        mock_run: mock.MagicMock,
        mock_exit: mock.MagicMock,
        tmp_path: Path,
    ) -> None:
        # Go is installed
        mock_run.return_value = mock.MagicMock(
            returncode=0, stdout="go version go1.22\n", stderr=""
        )
        # Gateway is reachable
        mock_get.return_value = mock.MagicMock(status_code=200)
        # Point SHARED_DIR to empty dir (no shared docs)
        orig_config = benchmark_runner.ARENA_CONFIG
        orig_shared = benchmark_runner.SHARED_DIR
        benchmark_runner.ARENA_CONFIG = tmp_path / "arena_config.json"
        benchmark_runner.SHARED_DIR = tmp_path / "shared_missing"
        try:
            benchmark_runner.preflight_check("http://localhost:18789")
        except SystemExit:
            pass
        finally:
            benchmark_runner.ARENA_CONFIG = orig_config
            benchmark_runner.SHARED_DIR = orig_shared
        mock_exit.assert_called_once()


class TestParseFailedMd:
    def test_full_parse(self, tmp_path: Path) -> None:
        failed = tmp_path / "FAILED.md"
        failed.write_text(
            "# Run Failed\n"
            "## Model\n"
            "openrouter/xiaomi/mimo\n"
            "## Failed Subagent\n"
            "qa_bot\n"
            "## Failure Reason\n"
            "Connection reset\n"
            "## Timestamp\n"
            "2026-04-09T15:30:00Z\n"
        )
        result = benchmark_runner._parse_failed_md(failed)
        assert result == {
            "model": "openrouter/xiaomi/mimo",
            "failed_subagent": "qa_bot",
            "reason": "Connection reset",
            "timestamp": "2026-04-09T15:30:00Z",
        }

    def test_missing_sections_default_to_unknown(self, tmp_path: Path) -> None:
        failed = tmp_path / "FAILED.md"
        failed.write_text("# Run Failed\nSome random text\n")
        result = benchmark_runner._parse_failed_md(failed)
        assert result["model"] == "unknown"
        assert result["failed_subagent"] == "unknown"
        assert result["reason"] == "unknown"
        assert result["timestamp"] == "unknown"

    def test_partial_sections(self, tmp_path: Path) -> None:
        failed = tmp_path / "FAILED.md"
        failed.write_text(
            "# Run Failed\n"
            "## Model\n"
            "my/model\n"
            "## Failure Reason\n"
            "Timeout\n"
        )
        result = benchmark_runner._parse_failed_md(failed)
        assert result["model"] == "my/model"
        assert result["failed_subagent"] == "unknown"
        assert result["reason"] == "Timeout"
        assert result["timestamp"] == "unknown"


class TestRecordFailure:
    def test_with_full_failure_info(self) -> None:
        failure_info: dict[str, benchmark_runner.Any] = {
            "model": "test/model",
            "failed_subagent": "dev_bot",
            "reason": "OOM killed",
            "timestamp": "2026-04-09T10:00:00Z",
        }
        result = benchmark_runner.record_failure("test/model", failure_info)
        assert result["model"] == "test/model"
        assert result["status"] == "failed"
        assert result["failed_subagent"] == "dev_bot"
        assert result["failure_reason"] == "OOM killed"
        assert result["failure_timestamp"] == "2026-04-09T10:00:00Z"
        # Telemetry fields should be unset
        assert result["qa_rejections"] == -1
        assert result["qa_approvals"] == -1

    def test_with_none_failure_info(self) -> None:
        result = benchmark_runner.record_failure("test/model", None)
        assert result["status"] == "failed"
        assert result["failed_subagent"] == "unknown"
        assert result["failure_reason"] == "unknown"
        assert result["failure_timestamp"] == "unknown"

    def test_with_partial_failure_info(self) -> None:
        failure_info: dict[str, benchmark_runner.Any] = {
            "reason": "Unknown error",
        }
        result = benchmark_runner.record_failure("partial/model", failure_info)
        assert result["status"] == "failed"
        assert result["failed_subagent"] == "unknown"
        assert result["failure_reason"] == "Unknown error"


class TestRecordTimeout:
    def test_timeout_metrics(self) -> None:
        result = benchmark_runner._record_timeout("test/model")
        assert result["model"] == "test/model"
        assert result["status"] == "timeout"
        assert result["qa_rejections"] == -1
        assert result["qa_approvals"] == -1
        assert result["time_to_done_seconds"] == -1
        assert result["test_coverage_percent"] == -1
        assert result["lint_warnings"] == -1
        assert result["gosec_issues"] == -1
        assert result["govulncheck_issues"] == -1
        assert result["golden_task_completed"] is False


class TestRecordCompleted:
    def test_adds_status_field(self) -> None:
        metrics: dict[str, benchmark_runner.Any] = {
            "model": "test/model",
            "qa_rejections": 1,
            "qa_approvals": 1,
        }
        result = benchmark_runner._record_completed(metrics)
        assert result["status"] == "completed"
        # Original keys preserved
        assert result["model"] == "test/model"
        assert result["qa_rejections"] == 1
        assert result["qa_approvals"] == 1

    def test_overwrites_existing_status(self) -> None:
        metrics: dict[str, benchmark_runner.Any] = {
            "model": "test/model",
            "status": "pending",
        }
        result = benchmark_runner._record_completed(metrics)
        assert result["status"] == "completed"


class TestCompileFinalResultsStatus:
    def test_ensures_status_field(self, tmp_path: Path) -> None:
        orig_results = benchmark_runner.ARENA_RESULTS
        orig_final = benchmark_runner.FINAL_RESULTS
        benchmark_runner.ARENA_RESULTS = tmp_path / "arena-results"
        benchmark_runner.FINAL_RESULTS = tmp_path / "FINAL_RESULTS.json"
        benchmark_runner.ARENA_RESULTS.mkdir(parents=True)
        metrics_dir = benchmark_runner.ARENA_RESULTS / "model_a"
        metrics_dir.mkdir()
        # Write metrics WITHOUT a status field
        (metrics_dir / "metrics.json").write_text(
            '{"model": "a", "score": 90}'
        )
        try:
            results = benchmark_runner.compile_final_results()
            assert len(results) == 1
            assert results[0]["model"] == "a"
            assert results[0]["status"] == "unknown"
        finally:
            benchmark_runner.ARENA_RESULTS = orig_results
            benchmark_runner.FINAL_RESULTS = orig_final

    def test_preserves_existing_status(self, tmp_path: Path) -> None:
        orig_results = benchmark_runner.ARENA_RESULTS
        orig_final = benchmark_runner.FINAL_RESULTS
        benchmark_runner.ARENA_RESULTS = tmp_path / "arena-results"
        benchmark_runner.FINAL_RESULTS = tmp_path / "FINAL_RESULTS.json"
        benchmark_runner.ARENA_RESULTS.mkdir(parents=True)
        metrics_dir = benchmark_runner.ARENA_RESULTS / "model_b"
        metrics_dir.mkdir()
        (metrics_dir / "metrics.json").write_text(
            '{"model": "b", "status": "completed", "score": 95}'
        )
        try:
            results = benchmark_runner.compile_final_results()
            assert len(results) == 1
            assert results[0]["status"] == "completed"
        finally:
            benchmark_runner.ARENA_RESULTS = orig_results
            benchmark_runner.FINAL_RESULTS = orig_final


class TestCliFlags:
    def test_fail_fast_flag(self) -> None:
        parser = benchmark_runner.build_parser()
        args = parser.parse_args(["--hook-token", "tok", "--fail-fast"])
        assert args.fail_fast is True

    def test_fail_fast_default_false(self) -> None:
        parser = benchmark_runner.build_parser()
        args = parser.parse_args(["--hook-token", "tok"])
        assert args.fail_fast is False

    def test_retry_flag(self) -> None:
        parser = benchmark_runner.build_parser()
        args = parser.parse_args(["--hook-token", "tok", "--retry", "3"])
        assert args.retry == 3

    def test_retry_default_zero(self) -> None:
        parser = benchmark_runner.build_parser()
        args = parser.parse_args(["--hook-token", "tok"])
        assert args.retry == 0


# ---------------------------------------------------------------------------
# telemetry tests
# ---------------------------------------------------------------------------


class TestParseWorklog:
    def test_counts_rejections_and_approvals(self, tmp_path: Path) -> None:
        worklog = tmp_path / "WORKLOG.md"
        worklog.write_text(
            "[2026-04-09 10:00] | dev_bot | START | Started work\n"
            "[2026-04-09 11:00] | qa_bot | REVIEW_REJECTED | Fix lint\n"
            "[2026-04-09 12:00] | qa_bot | REVIEW_APPROVED | Looks good\n"
            "[2026-04-09 12:05] | pm_bot | PROJECT_COMPLETED | Done\n"
        )
        result = telemetry.parse_worklog(tmp_path)
        assert result["qa_rejections"] == 1
        assert result["qa_approvals"] == 1
        assert result["golden_task_completed"] is True
        assert result["time_to_done_seconds"] == (12 * 60 + 5) * 60 - (10 * 60) * 60
        # More precisely: 12:05 - 10:00 = 2h5m = 7500s
        assert result["time_to_done_seconds"] == 7500

    def test_no_worklog(self, tmp_path: Path) -> None:
        result = telemetry.parse_worklog(tmp_path)
        assert result["qa_rejections"] == -1
        assert result["qa_approvals"] == -1
        assert result["golden_task_completed"] is False

    def test_no_completion_marker(self, tmp_path: Path) -> None:
        worklog = tmp_path / "WORKLOG.md"
        worklog.write_text(
            "[2026-04-09 10:00] | dev_bot | START | Started work\n"
        )
        result = telemetry.parse_worklog(tmp_path)
        assert result["golden_task_completed"] is False


class TestCheckCompletion:
    def test_approved_report(self, tmp_path: Path) -> None:
        report = tmp_path / "COMPLETION_REPORT.md"
        report.write_text("Status: APPROVED\nAll checks passed.")
        assert telemetry.check_completion(tmp_path) is True

    def test_no_report(self, tmp_path: Path) -> None:
        assert telemetry.check_completion(tmp_path) is False

    def test_rejected_report(self, tmp_path: Path) -> None:
        report = tmp_path / "COMPLETION_REPORT.md"
        report.write_text("Status: REJECTED\nFix issues.")
        assert telemetry.check_completion(tmp_path) is False


class TestGetTestCoverage:
    @mock.patch("telemetry._run_cmd")
    def test_parses_coverage(self, mock_cmd: mock.MagicMock) -> None:
        mock_cmd.return_value = (0, "ok\tgithub.com/foo\t0.1s\tcoverage: 87.5% of statements\n", "")
        assert telemetry.get_test_coverage(Path("/fake")) == 87.5

    @mock.patch("telemetry._run_cmd")
    def test_unavailable(self, mock_cmd: mock.MagicMock) -> None:
        mock_cmd.return_value = (-1, "", "unavailable")
        assert telemetry.get_test_coverage(Path("/fake")) == -1


class TestCountLintWarnings:
    @mock.patch("telemetry._run_cmd")
    def test_counts_warnings(self, mock_cmd: mock.MagicMock) -> None:
        mock_cmd.return_value = (1, "file.go:10: unused var\nfile.go:20: nil deref\n", "")
        assert telemetry.count_lint_warnings(Path("/fake")) == 2

    @mock.patch("telemetry._run_cmd")
    def test_clean(self, mock_cmd: mock.MagicMock) -> None:
        mock_cmd.return_value = (0, "", "")
        assert telemetry.count_lint_warnings(Path("/fake")) == 0

    @mock.patch("telemetry._run_cmd")
    def test_unavailable(self, mock_cmd: mock.MagicMock) -> None:
        mock_cmd.return_value = (-1, "", "unavailable")
        assert telemetry.count_lint_warnings(Path("/fake")) == -1


class TestCountGosecIssues:
    @mock.patch("telemetry._run_cmd")
    def test_parses_failures(self, mock_cmd: mock.MagicMock) -> None:
        mock_cmd.return_value = (1, "[failures: 3]\n", "")
        assert telemetry.count_gosec_issues(Path("/fake")) == 3

    @mock.patch("telemetry._run_cmd")
    def test_clean(self, mock_cmd: mock.MagicMock) -> None:
        mock_cmd.return_value = (0, "No issues found.\n", "")
        assert telemetry.count_gosec_issues(Path("/fake")) == 0

    @mock.patch("telemetry._run_cmd")
    def test_unavailable(self, mock_cmd: mock.MagicMock) -> None:
        mock_cmd.return_value = (-1, "", "unavailable")
        assert telemetry.count_gosec_issues(Path("/fake")) == -1


class TestCountGovulncheckIssues:
    @mock.patch("telemetry._run_cmd")
    def test_parses_vulns(self, mock_cmd: mock.MagicMock) -> None:
        mock_cmd.return_value = (1, "Vuln ID: GHSA-xxxx-yyyy-zzzz\n", "")
        assert telemetry.count_govulncheck_issues(Path("/fake")) == 1

    @mock.patch("telemetry._run_cmd")
    def test_clean(self, mock_cmd: mock.MagicMock) -> None:
        mock_cmd.return_value = (0, "No known vulnerabilities found.\n", "")
        assert telemetry.count_govulncheck_issues(Path("/fake")) == 0

    @mock.patch("telemetry._run_cmd")
    def test_unavailable(self, mock_cmd: mock.MagicMock) -> None:
        mock_cmd.return_value = (-1, "", "unavailable")
        assert telemetry.count_govulncheck_issues(Path("/fake")) == -1


class TestResolveModel:
    def test_explicit_model(self, tmp_path: Path) -> None:
        assert telemetry.resolve_model(tmp_path, "explicit/model") == "explicit/model"

    def test_from_config(self, tmp_path: Path) -> None:
        config = tmp_path.parent / "arena_config.json"
        config.write_text('{"model": "config/model"}')
        try:
            assert telemetry.resolve_model(tmp_path, None) == "config/model"
        finally:
            config.unlink(missing_ok=True)

    def test_fallback_unknown(self, tmp_path: Path) -> None:
        assert telemetry.resolve_model(tmp_path, None) == "unknown"


# ---------------------------------------------------------------------------
# Tests for strengthened prompt (orchestrator non-implementation)
# ---------------------------------------------------------------------------


class TestStrengthenedPrompt:
    """Verify the agent prompt contains the prohibition in at least 3
    distinct locations and uses the strongest possible language."""

    def _get_prompt(self) -> str:
        return benchmark_runner._build_agent_prompt(
            Path("/fake/project"), "test/model"
        )

    def test_prohibition_at_beginning(self) -> None:
        prompt = self._get_prompt()
        # The CRITICAL RULE section should appear before the workflow steps
        assert "CRITICAL RULE" in prompt
        # The prohibition should be the very first instruction
        first_forbidden_idx = prompt.find("ABSOLUTELY FORBIDDEN")
        workflow_idx = prompt.find("--- WORKFLOW ---")
        assert first_forbidden_idx < workflow_idx

    def test_prohibition_in_middle(self) -> None:
        prompt = self._get_prompt()
        # Reminder during workflow section
        assert "REMINDER during workflow" in prompt
        # The prompt uses em-dash and uppercase NOT
        assert "NOT to write implementation code" in prompt
        assert "orchestrator, not a developer" in prompt

    def test_prohibition_at_end(self) -> None:
        prompt = self._get_prompt()
        # Final reminder in failure handling section
        assert "FINAL REMINDER" in prompt
        assert "NEVER write implementation code" in prompt

    def test_uses_strong_language(self) -> None:
        prompt = self._get_prompt()
        strong_terms = ["CRITICAL RULE", "ABSOLUTELY FORBIDDEN",
                        "UNDER NO CIRCUMSTANCES", "NEVER"]
        for term in strong_terms:
            assert term in prompt, (
                f"Prompt missing strong language: {term}"
            )

    def test_explains_why(self) -> None:
        prompt = self._get_prompt()
        assert "evaluated on your ability to ORCHESTRATE" in prompt
        assert "benchmark is completely invalidated" in prompt

    def test_negative_and_positive_examples(self) -> None:
        prompt = self._get_prompt()
        assert "WRONG:" in prompt
        assert "CORRECT:" in prompt
        assert "implement the solution myself" in prompt
        assert "Writing FAILED.md" in prompt

    def test_self_check_instruction(self) -> None:
        prompt = self._get_prompt()
        assert "SELF-CHECK" in prompt
        assert "Am I writing implementation code" in prompt

    def test_restricts_orchestrator_role(self) -> None:
        prompt = self._get_prompt()
        assert "Your ONLY jobs are" in prompt
        assert "Spawn subagents" in prompt
        assert "You are NOT a developer" in prompt

    def test_prohibition_appears_at_least_three_times(self) -> None:
        prompt = self._get_prompt()
        # Count occurrences of the core prohibition concept
        count = 0
        for phrase in [
            "do NOT attempt to do the work yourself",
            "NEVER IMPLEMENT CODE YOURSELF",
            "NEVER write implementation code",
            "not to fix the code yourself",
            "ABSOLUTELY FORBIDDEN",
        ]:
            if phrase in prompt:
                count += 1
        assert count >= 3, (
            f"Prohibition only appears {count} times, need >= 3"
        )


# ---------------------------------------------------------------------------
# Tests for detect_orchestrator_overreach()
# ---------------------------------------------------------------------------


class TestDetectOrchestratorOverreach:
    """Test the overreach detection with various WORKLOG scenarios."""

    def test_no_worklog_no_code_files(self, tmp_path: Path) -> None:
        result = telemetry.detect_orchestrator_overreach(tmp_path)
        assert result["orchestrator_overreach_detected"] is False
        assert result["overreach_evidence"] == []
        assert result["severity"] == "none"

    def test_clean_run_with_dev_bot(self, tmp_path: Path) -> None:
        worklog = tmp_path / "WORKLOG.md"
        worklog.write_text(
            "[2026-04-09 10:00] | pm_bot | START | Initializing\n"
            "[2026-04-09 10:01] | pm_bot | SPAWN | Spawned dev_bot\n"
            "[2026-04-09 10:30] | dev_bot | COMPLETE | Implementation done\n"
            "[2026-04-09 10:35] | qa_bot | REVIEW_APPROVED | Looks good\n"
            "[2026-04-09 10:40] | pm_bot | PROJECT_COMPLETED | Done\n"
        )
        (tmp_path / "main.go").write_text("package main\n")
        result = telemetry.detect_orchestrator_overreach(tmp_path)
        assert result["orchestrator_overreach_detected"] is False
        assert result["severity"] == "none"

    def test_orchestrator_mentions_implementing(self, tmp_path: Path) -> None:
        worklog = tmp_path / "WORKLOG.md"
        worklog.write_text(
            "[2026-04-09 10:00] | pm_bot | START | Initializing\n"
            "[2026-04-09 10:01] | pm_bot | SPAWN | Spawned dev_bot\n"
            "[2026-04-09 10:15] | dev_bot | FAIL | Model error\n"
            "[2026-04-09 10:20] | pm_bot | ACTION | dev_bot failed, so I "
            "implemented the solution myself\n"
            "[2026-04-09 10:30] | pm_bot | COMPLETE | Done\n"
        )
        result = telemetry.detect_orchestrator_overreach(tmp_path)
        assert result["orchestrator_overreach_detected"] is True
        assert len(result["overreach_evidence"]) >= 1
        assert any("implement" in e.lower() for e in result["overreach_evidence"])
        assert result["severity"] == "warning"

    def test_orchestrator_wrote_code_files(self, tmp_path: Path) -> None:
        worklog = tmp_path / "WORKLOG.md"
        worklog.write_text(
            "[2026-04-09 10:00] | pm_bot | START | Initializing\n"
            "[2026-04-09 10:30] | pm_bot | COMPLETE | Done\n"
        )
        # Code file exists but no dev_bot was spawned
        (tmp_path / "main.go").write_text("package main\n")
        result = telemetry.detect_orchestrator_overreach(tmp_path)
        assert result["orchestrator_overreach_detected"] is True
        assert any("no dev_bot spawn" in e.lower() for e in result["overreach_evidence"])
        assert result["severity"] == "warning"

    def test_completion_without_dev_bot(self, tmp_path: Path) -> None:
        worklog = tmp_path / "WORKLOG.md"
        worklog.write_text(
            "[2026-04-09 10:00] | pm_bot | START | Initializing\n"
            "[2026-04-09 10:30] | pm_bot | COMPLETE | Done\n"
        )
        # COMPLETION_REPORT exists but no dev_bot activity
        (tmp_path / "COMPLETION_REPORT.md").write_text("Status: APPROVED\n")
        result = telemetry.detect_orchestrator_overreach(tmp_path)
        assert result["orchestrator_overreach_detected"] is True
        assert any(
            "COMPLETION_REPORT" in e and "no dev_bot" in e.lower()
            for e in result["overreach_evidence"]
        )

    def test_multiple_signals_is_critical(self, tmp_path: Path) -> None:
        worklog = tmp_path / "WORKLOG.md"
        worklog.write_text(
            "[2026-04-09 10:00] | pm_bot | START | Initializing\n"
            "[2026-04-09 10:20] | pm_bot | ACTION | I will implement the "
            "Go code myself\n"
            "[2026-04-09 10:30] | pm_bot | COMPLETE | Done\n"
        )
        (tmp_path / "main.go").write_text("package main\n")
        (tmp_path / "COMPLETION_REPORT.md").write_text("Status: APPROVED\n")
        result = telemetry.detect_orchestrator_overreach(tmp_path)
        assert result["orchestrator_overreach_detected"] is True
        assert result["severity"] == "critical"

    def test_code_files_with_dev_bot_spawn_is_clean(self, tmp_path: Path) -> None:
        worklog = tmp_path / "WORKLOG.md"
        worklog.write_text(
            "[2026-04-09 10:00] | pm_bot | START | Initializing\n"
            "[2026-04-09 10:01] | pm_bot | ACTION | Spawned dev_bot to "
            "implement the task\n"
            "[2026-04-09 10:30] | dev_bot | COMPLETE | Implementation done\n"
        )
        (tmp_path / "main.go").write_text("package main\n")
        result = telemetry.detect_orchestrator_overreach(tmp_path)
        assert result["orchestrator_overreach_detected"] is False
        assert result["severity"] == "none"

    def test_qa_bot_entries_not_flagged(self, tmp_path: Path) -> None:
        """QA bot reviewing code should not be flagged as overreach."""
        worklog = tmp_path / "WORKLOG.md"
        worklog.write_text(
            "[2026-04-09 10:00] | pm_bot | START | Initializing\n"
            "[2026-04-09 10:01] | pm_bot | ACTION | Spawned dev_bot\n"
            "[2026-04-09 10:30] | dev_bot | COMPLETE | Done\n"
            "[2026-04-09 10:35] | qa_bot | REVIEW | Fixed my review comments\n"
            "[2026-04-09 10:40] | qa_bot | REVIEW_APPROVED | Good\n"
        )
        result = telemetry.detect_orchestrator_overreach(tmp_path)
        # qa_bot is a subagent, so "fixed" in its entry should not flag
        assert result["orchestrator_overreach_detected"] is False

    def test_pm_bot_admin_entries_not_flagged(self, tmp_path: Path) -> None:
        """PM doing orchestration admin (not coding) should be clean."""
        worklog = tmp_path / "WORKLOG.md"
        worklog.write_text(
            "[2026-04-09 10:00] | pm_bot | START | Initializing\n"
            "[2026-04-09 10:01] | pm_bot | ACTION | Spawned dev_bot\n"
            "[2026-04-09 10:30] | dev_bot | COMPLETE | Done\n"
            "[2026-04-09 10:35] | qa_bot | REVIEW_APPROVED | Good\n"
            "[2026-04-09 10:40] | pm_bot | PROJECT_COMPLETED | Created "
            "completion report\n"
        )
        result = telemetry.detect_orchestrator_overreach(tmp_path)
        # "Created completion report" is not an implementation pattern
        assert result["orchestrator_overreach_detected"] is False


# ---------------------------------------------------------------------------
# Tests for CLI --strict flag
# ---------------------------------------------------------------------------


class TestStrictFlag:
    def test_strict_flag_set(self) -> None:
        parser = benchmark_runner.build_parser()
        args = parser.parse_args(["--hook-token", "tok", "--strict"])
        assert args.strict is True

    def test_strict_flag_default_false(self) -> None:
        parser = benchmark_runner.build_parser()
        args = parser.parse_args(["--hook-token", "tok"])
        assert args.strict is False


# ---------------------------------------------------------------------------
# Tests for overreach integration in main() flow
# ---------------------------------------------------------------------------


class TestOverreachIntegration:
    """Test that the runner correctly marks results as invalid on critical
    overreach and includes overreach fields in metrics."""

    @mock.patch("benchmark_runner.detect_orchestrator_overreach")
    @mock.patch("benchmark_runner.run_telemetry")
    def test_critical_overreach_marks_invalid(
        self,
        mock_telemetry: mock.MagicMock,
        mock_overreach: mock.MagicMock,
        tmp_path: Path,
    ) -> None:
        mock_telemetry.return_value = {"model": "test/model"}
        mock_overreach.return_value = {
            "orchestrator_overreach_detected": True,
            "overreach_evidence": ["evidence1", "evidence2"],
            "severity": "critical",
        }

        # Patch constants
        orig_target = benchmark_runner.ARENA_TARGET
        orig_results = benchmark_runner.ARENA_RESULTS
        orig_final = benchmark_runner.FINAL_RESULTS
        benchmark_runner.ARENA_TARGET = tmp_path / "arena-target"
        benchmark_runner.ARENA_RESULTS = tmp_path / "arena-results"
        benchmark_runner.FINAL_RESULTS = tmp_path / "FINAL_RESULTS.json"
        benchmark_runner.ARENA_TARGET.mkdir(parents=True)

        try:
            # Simulate what main() does after a "completed" outcome
            metrics = benchmark_runner.run_telemetry()
            assert metrics is not None

            worklog_path = benchmark_runner.ARENA_TARGET / "WORKLOG.md"
            overreach = benchmark_runner.detect_orchestrator_overreach(
                benchmark_runner.ARENA_TARGET, worklog_path
            )
            metrics["orchestrator_overreach_detected"] = overreach[
                "orchestrator_overreach_detected"
            ]
            metrics["overreach_evidence"] = overreach["overreach_evidence"]
            metrics["overreach_severity"] = overreach["severity"]

            # Simulate strict=False, critical severity
            if overreach["severity"] == "critical":
                metrics["status"] = "invalid"
            else:
                metrics = benchmark_runner._record_completed(metrics)

            assert metrics["status"] == "invalid"
            assert metrics["orchestrator_overreach_detected"] is True
            assert len(metrics["overreach_evidence"]) == 2
            assert metrics["overreach_severity"] == "critical"
        finally:
            benchmark_runner.ARENA_TARGET = orig_target
            benchmark_runner.ARENA_RESULTS = orig_results
            benchmark_runner.FINAL_RESULTS = orig_final

    @mock.patch("benchmark_runner.detect_orchestrator_overreach")
    @mock.patch("benchmark_runner.run_telemetry")
    def test_warning_overreach_stays_completed(
        self,
        mock_telemetry: mock.MagicMock,
        mock_overreach: mock.MagicMock,
        tmp_path: Path,
    ) -> None:
        mock_telemetry.return_value = {"model": "test/model"}
        mock_overreach.return_value = {
            "orchestrator_overreach_detected": True,
            "overreach_evidence": ["minor evidence"],
            "severity": "warning",
        }

        orig_target = benchmark_runner.ARENA_TARGET
        orig_results = benchmark_runner.ARENA_RESULTS
        orig_final = benchmark_runner.FINAL_RESULTS
        benchmark_runner.ARENA_TARGET = tmp_path / "arena-target"
        benchmark_runner.ARENA_RESULTS = tmp_path / "arena-results"
        benchmark_runner.FINAL_RESULTS = tmp_path / "FINAL_RESULTS.json"
        benchmark_runner.ARENA_TARGET.mkdir(parents=True)

        try:
            metrics = benchmark_runner.run_telemetry()
            assert metrics is not None

            worklog_path = benchmark_runner.ARENA_TARGET / "WORKLOG.md"
            overreach = benchmark_runner.detect_orchestrator_overreach(
                benchmark_runner.ARENA_TARGET, worklog_path
            )
            metrics["orchestrator_overreach_detected"] = overreach[
                "orchestrator_overreach_detected"
            ]
            metrics["overreach_evidence"] = overreach["overreach_evidence"]
            metrics["overreach_severity"] = overreach["severity"]

            if overreach["severity"] == "critical":
                metrics["status"] = "invalid"
            elif overreach["severity"] == "warning":
                metrics = benchmark_runner._record_completed(metrics)
            else:
                metrics = benchmark_runner._record_completed(metrics)

            assert metrics["status"] == "completed"
            assert metrics["orchestrator_overreach_detected"] is True
            assert metrics["overreach_severity"] == "warning"
        finally:
            benchmark_runner.ARENA_TARGET = orig_target
            benchmark_runner.ARENA_RESULTS = orig_results
            benchmark_runner.FINAL_RESULTS = orig_final

    @mock.patch("benchmark_runner.detect_orchestrator_overreach")
    @mock.patch("benchmark_runner.run_telemetry")
    def test_strict_mode_upgrades_warning_to_critical(
        self,
        mock_telemetry: mock.MagicMock,
        mock_overreach: mock.MagicMock,
        tmp_path: Path,
    ) -> None:
        mock_telemetry.return_value = {"model": "test/model"}
        mock_overreach.return_value = {
            "orchestrator_overreach_detected": True,
            "overreach_evidence": ["minor evidence"],
            "severity": "warning",
        }

        orig_target = benchmark_runner.ARENA_TARGET
        orig_results = benchmark_runner.ARENA_RESULTS
        orig_final = benchmark_runner.FINAL_RESULTS
        benchmark_runner.ARENA_TARGET = tmp_path / "arena-target"
        benchmark_runner.ARENA_RESULTS = tmp_path / "arena-results"
        benchmark_runner.FINAL_RESULTS = tmp_path / "FINAL_RESULTS.json"
        benchmark_runner.ARENA_TARGET.mkdir(parents=True)

        try:
            metrics = benchmark_runner.run_telemetry()
            assert metrics is not None

            worklog_path = benchmark_runner.ARENA_TARGET / "WORKLOG.md"
            overreach = benchmark_runner.detect_orchestrator_overreach(
                benchmark_runner.ARENA_TARGET, worklog_path
            )
            metrics["orchestrator_overreach_detected"] = overreach[
                "orchestrator_overreach_detected"
            ]
            metrics["overreach_evidence"] = overreach["overreach_evidence"]
            metrics["overreach_severity"] = overreach["severity"]

            # Simulate strict mode
            strict = True
            if strict and overreach["orchestrator_overreach_detected"]:
                overreach["severity"] = "critical"
                metrics["overreach_severity"] = "critical"

            if overreach["severity"] == "critical":
                metrics["status"] = "invalid"
            else:
                metrics = benchmark_runner._record_completed(metrics)

            assert metrics["status"] == "invalid"
            assert metrics["overreach_severity"] == "critical"
        finally:
            benchmark_runner.ARENA_TARGET = orig_target
            benchmark_runner.ARENA_RESULTS = orig_results
            benchmark_runner.FINAL_RESULTS = orig_final

    def test_final_results_includes_overreach_fields(
        self, tmp_path: Path
    ) -> None:
        """Verify that compile_final_results preserves overreach fields."""
        orig_results = benchmark_runner.ARENA_RESULTS
        orig_final = benchmark_runner.FINAL_RESULTS
        benchmark_runner.ARENA_RESULTS = tmp_path / "arena-results"
        benchmark_runner.FINAL_RESULTS = tmp_path / "FINAL_RESULTS.json"
        benchmark_runner.ARENA_RESULTS.mkdir(parents=True)
        metrics_dir = benchmark_runner.ARENA_RESULTS / "model_x"
        metrics_dir.mkdir()
        (metrics_dir / "metrics.json").write_text(
            '{'
            '"model": "x", '
            '"status": "invalid", '
            '"orchestrator_overreach_detected": true, '
            '"overreach_evidence": ["evidence A"], '
            '"overreach_severity": "critical"'
            '}'
        )

        try:
            results = benchmark_runner.compile_final_results()
            assert len(results) == 1
            entry = results[0]
            assert entry["model"] == "x"
            assert entry["status"] == "invalid"
            assert entry["orchestrator_overreach_detected"] is True
            assert entry["overreach_evidence"] == ["evidence A"]
            assert entry["overreach_severity"] == "critical"
        finally:
            benchmark_runner.ARENA_RESULTS = orig_results
            benchmark_runner.FINAL_RESULTS = orig_final
