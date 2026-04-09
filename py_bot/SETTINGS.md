# py_bot Settings

**Model:** `openrouter/kwaipilot/kat-coder-pro-v2`
**Purpose:** Python development, FastAPI, Docker/SSH automation

## Project

| Field | Value |
|-------|-------|
| Project | Amnezia Web Panel |
| Language | Python 3.10+ |
| Framework | FastAPI + Starlette |
| Formatter | black (line-length=100) |
| Linter | flake8 (max-line-length=100) |
| Test Runner | pytest --cov=. --cov-report=term-missing |

## Quality Gates

| Gate | Must Pass | Command |
|------|-----------|---------|
| black | Yes | `black .` |
| flake8 | Yes | `flake8 .` |
| pytest | Yes | `pytest -v` |
| pip-audit | Yes | `pip-audit` |

## Project Paths

| Path | Description |
|------|-------------|
| `app.py` | FastAPI entry point |
| `ssh_manager.py` | SSH connection manager |
| `awg_manager.py` | WireGuard manager |
| `xray_manager.py` | Xray/VLESS-Reality manager |
| `dns_manager.py` | DNS manager |
| `telemt_manager.py` | TELMT manager |
| `telegram_bot.py` | Telegram bot |
| `tests/` | Unit tests |
| `templates/` | Jinja2 templates |
| `translations/` | i18n JSON files |
