# AI Development Team Workflow

## Process Overview
1. **Planning** - PM receives request and breaks into tasks
2. **Development** - Dev implements features in Golang
3. **Review** - QA audits code for quality, security, and correctness
4. **Iteration** - Feedback loop until QA approves
5. **Completion** - PM confirms "done-done" and reports to human

## Communication Channels
- **Task Assignment**: PM → Dev (specific implementation tasks)
- **Review Request**: PM → QA (code to review)
- **Feedback**: QA → PM (review comments and approval status)
- **Status Updates**: PM → Human (progress and completion reports)

## Definition of Done
A task is considered "done-done" when:
1. Code is implemented by dev_bot
2. Code passes review by qa_bot (no critical issues)
3. **All three security tools pass clean** (golangci-lint, gosec, govulncheck) — mandatory, no exceptions
4. All tests pass
5. Code follows Go best practices
6. PM has verified completion and reported to human

## Escalation Path
- If dev_bot and qa_bot disagree on implementation, PM mediates
- If human needs clarification, PM interfaces directly
- Blocking issues are highlighted immediately by QA