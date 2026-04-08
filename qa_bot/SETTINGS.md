# qa_bot - Settings

## Model Configuration

**Current Model:** openrouter/kwaipilot/kat-coder-pro-v2

### Model Details
| Field | Value |
|-------|-------|
| **Provider** | OpenRouter |
| **Model** | kwaipilot/kat-coder-pro-v2 |
| **Purpose** | Multi-language code review (Go + Python), security scanning |
| **Context Window** | ~32k tokens |

### Model History
| Date | Model | Notes |
|------|-------|-------|
| 2026-03-21 | kwaipilot/kat-coder-pro-v2 | Initial configuration |

## Review Configuration

### Review Priorities
1. Security vulnerabilities (Critical)
2. Bug detection (High)
3. Code quality and idioms (High)
4. Test coverage adequacy (Medium)
5. Performance concerns (Medium)

### Review Standards
- Security-first approach
- Actionable feedback only
- No blocking on pure style preferences
- Language-idiom aware (Go idioms for dev_bot, Python idioms for py_bot)

## Tools Installed

### Go Tools
| Tool | Version | Purpose |
|------|---------|---------|
| `golangci-lint` | v1.64.8 | Aggregated linter (50+ linters) |
| `gosec` | latest | Go security scanner |
| `govulncheck` | v1.1.4 | Dependency CVE scanner |

### Python Tools
| Tool | Version | Purpose |
|------|---------|---------|
| `black` | 25.1.0 | Code formatter |
| `flake8` | 7.1.1 | Linter |
| `ruff` | latest | Aggressive linter / logic checker |
| `bandit` | latest | Python security vulnerability scanner |
| `mypy` | latest | Static type checker |
| `pytest` | 8.3.5 | Test runner |
| `pytest-cov` | 6.1.1 | Coverage reporter |
| `pip-audit` | 2.10.0 | Dependency CVE scanner |

## Quality Gates

### Go Projects (dev_bot)
| Gate | Must Pass? | Notes |
|------|-----------|-------|
| go fmt | Yes | Code formatted |
| go vet | Yes | No warnings |
| golangci-lint | Yes | No critical/high issues |
| gosec | Yes | No critical/high security issues |
| govulncheck | Yes | No known vulnerability CVEs |
| go build | Yes | Compiles clean |
| go test | Yes | All tests pass |
| Test coverage | No | Target ≥80% but not blocking |

### Python Projects (py_bot)
| Gate | Must Pass? | Notes |
|------|-----------|-------|
| black | Yes | Code formatted |
| flake8 | Yes | No errors |
| mypy | Yes (if installed) | No type errors |
| pytest | Yes | All tests pass |
| pip-audit | Yes | No known CVEs |
| Test coverage | No | Target ≥80% but not blocking |

## Language Detection

When assigned a review, detect the project language from:
- `go.mod` → Go review
- `requirements.txt` / `pyproject.toml` → Python review
- If mixed, run both tool sets

## Review Output Format

Every review report must include:
1. **Summary** — one line: APPROVED / APPROVED WITH NOTES / REJECTED
2. **Tool outputs** — raw output from each tool run (or "clean")
3. **Findings** — categorized by severity (Critical / High / Medium / Low)
4. **Recommendations** — actionable fixes for each finding
5. **Coverage** — test coverage report if available
