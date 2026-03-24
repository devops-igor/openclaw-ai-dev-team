# qa_bot - Settings

## Model Configuration

**Current Model:** openrouter/xiaomi/mimo-v2-pro

### Model Details
- **Provider:** OpenRouter
- **Model:** xiaomi/mimo-v2-pro
- **Purpose:** Code review, security scanning, quality assurance
- **Context Window:** 32768 tokens (estimated)

### Model History
| Date | Model | Notes |
|------|-------|-------|
| 2026-03-21 | xiaomi/mimo-v2-pro | Switched from minimax-m2.7:cloud for improved code review |

## Review Configuration

### Review Priorities
1. Security vulnerabilities (Critical)
2. Bug detection (High)
3. Code quality and idioms (High)
4. Test coverage adequacy (Medium)
5. Performance concerns (Medium)

### Review Standards
- Follows GOLANG_STANDARDS.md
- Security-first approach
- Actionable feedback only
- No blocking on style preferences

### Turnaround Time
- Initial review: < 4 hours
- Follow-up review: < 2 hours
- Security scan: < 1 hour

## Quality Gates

| Gate | Must Pass? | Notes |
|------|-----------|-------|
| go vet | Yes | No warnings |
| go fmt | Yes | Code formatted |
| Security scan | Yes | No critical/high issues |
| Test coverage | No | Target ≥80% but not blocking |
