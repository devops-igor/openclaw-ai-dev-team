# CI/CD Errors

**Last checked:** YYYY-MM-DD HH:MM

## Active Failures

_No active failures._

---

## Historical Failures

_Records of past pipeline failures for reference._

---

**Document Purpose:** This file is maintained by `git_bot` as the pipeline watchdog output. When a CI/CD pipeline fails, this file is updated with the error summary and log excerpt. It serves as a centralized record of build failures across all projects.

**git_bot Process:**
1. Run `gh run list --status failure` to find failed workflow runs
2. For each failure, run `gh run view <run-id> --log-failed` to get error details
3. Overwrite this file entirely with a fresh report (always include timestamp)
4. If no failures found, write "No active failures" with timestamp
5. Escalate critical failures (security, secret leaks, blocks release) to pm_bot immediately
