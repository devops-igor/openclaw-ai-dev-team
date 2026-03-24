# Golang Development Standards

## Code Style
- Follow [Effective Go](https://golang.org/doc/effective_go.html)
- Use gofmt for formatting
- Use golint/golangci-lint for linting
- Group imports: standard library, third-party, local
- Keep lines reasonable length (<120 chars)

## Naming Conventions
- MixedCaps for exported names
- camelCase for unexported names
- Interface names ending in -er when single method (Reader, Writer)
- Avoid getters/setters unless necessary (use fields directly)

## Error Handling
- Check all errors explicitly
- Return early on errors when possible
- Wrap errors with context using fmt.Errorf or errors.Wrap
- Don't ignore errors with _ unless intentionally discarding
- Provide meaningful error messages

## Concurrency
- Prefer channels over mutexes for goroutine communication
- Use sync.WaitGroup for coordinating goroutine completion
- Context package for cancellation and timeouts
- Test for race conditions with `go test -race`

## Testing
- Table-driven tests when appropriate
- Test both positive and negative cases
- Mock external dependencies
- Aim for >80% coverage on critical paths
- Use testing package built-in, avoid over-mocking

## Security
- Validate all inputs
- Use proper authentication and authorization
- Sanitize outputs to prevent injection
- Use constant-time comparison for secrets
- Keep dependencies updated

## Documentation

### Project Documentation
Every project must include:
- `README.md` - Project overview, setup, usage
- `WORKLOG.md` - Append-only action log (prevents context window memory loss)
- `TASK.md`, `DEV_HANDOVER.md`, `QA_REPORT.md`, `COMPLETION_REPORT.md` - Handoff documents as per HANDOVER_PROTOCOL.md

### WORKLOG.md Requirements
- **Append-only:** Never edit or delete previous entries
- **Log all major actions:** task starts, decisions, handoffs, tests, reviews, blockers, deployments
- **Use format:** `YYYY-MM-DD HH:MM | AGENT | ACTION_TYPE | DESCRIPTION`
- **Part of Definition of Done:** No entry = work not complete
- See `shared/WORKLOG_TEMPLATE.md` for full guidelines

### Code Documentation
- Godoc comments for all exported functions, types, and packages
- Inline comments for complex or non-obvious logic
- Document edge cases and error conditions
- Keep comments up-to-date with code changes

### Commit Messages
(If using version control)
- Imperative mood: "Fix bug" not "Fixed bug"
- Short summary (50 chars) + detailed body
- Reference task IDs (e.g., "Implements TASK-001")
- Explain why, not what