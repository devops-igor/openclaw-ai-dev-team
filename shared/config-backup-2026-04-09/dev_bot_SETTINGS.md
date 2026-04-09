# dev_bot Settings

**Model:** `openrouter/kwaipilot/kat-coder-pro-v2`  
**Purpose:** Go development, code generation, implementation  
**Fallback:** `openrouter/stepfun/step-3.5-flash:free` → escalate to pm_bot if unavailable

## Pre-Handoff Checklist (run before handing to qa_bot)
```bash
go fmt ./... && go vet ./... && go test -race ./...
golangci-lint run ./...   # if available
```
Attach output to `DEV_HANDOVER.md`. Fix failures before handoff.

## Commit Rule
**NEVER run `git commit` or `git push`.** Hand off to git_bot via pm_bot.
