# qa_bot Settings

**Model:** `openrouter/kwaipilot/kat-coder-pro-v2`  
**Purpose:** Multi-language code review (Go + Python), security scanning

## Quality Gates

### Go
| Gate | Must Pass? |
|------|-----------|
| go fmt / vet / build / test | Yes |
| golangci-lint / gosec / govulncheck | Yes (no critical/high) |

### Python
| Gate | Must Pass? |
|------|-----------|
| black / flake8 | Yes |
| pytest / pip-audit | Yes |
| mypy | Yes (if installed) |
| Test coverage | Target ≥80%, non-blocking |

## Tools Installed
- **Go:** golangci-lint v1.64.8, gosec (latest), govulncheck v1.1.4
- **Python:** black 25.1.0, flake8 7.1.1, ruff, bandit, mypy, pytest 8.3.5, pytest-cov 6.1.1, pip-audit 2.10.0

## Review Priorities
1. Security (Critical)
2. Bug detection (High)
3. Code quality & idioms (High)
4. Test coverage (Medium)
5. Performance (Medium)
