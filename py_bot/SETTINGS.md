# py_bot - Settings

## Model Configuration

**Current Model:** openrouter/kwaipilot/kat-coder-pro-v2

### Model Details
| Field | Value |
|-------|-------|
| **Provider** | OpenRouter |
| **Model** | kwaipilot/kat-coder-pro-v2 |
| **Purpose** | Python development, FastAPI, Docker/SSH automation |
| **Context Window** | ~32k tokens |

### Model History
| Date | Model | Notes |
|------|-------|-------|
| 2026-04-08 | kwaipilot/kat-coder-pro-v2 | Initial configuration |

## Project Configuration

| Field | Value |
|-------|-------|
| **Project** | Amnezia Web Panel |
| **Language** | Python 3.10+ |
| **Framework** | FastAPI + Starlette |
| **Linter** | flake8 (max-line-length = 100) |
| **Formatter** | black (line-length = 100) |
| **Test Runner** | pytest --cov=. --cov-report=term-missing |

## Code Quality Gates

| Gate | Must Pass? | Command |
|------|-----------|---------|
| black formatting | Yes | `black .` |
| flake8 lint | Yes | `flake8 .` |
| pytest | Yes | `pytest -v` |
| pip-audit | Yes | `pip-audit` |

## Tools Available

| Tool | Purpose |
|------|---------|
| `black` | Code formatter |
| `flake8` | Linter |
| `pytest` | Test runner |
| `pytest-cov` | Coverage report |
| `pip-audit` | Dependency vulnerability scanner |

## Project Paths

| Path | Description |
|------|-------------|
| `/home/igor/Amnezia-Web-Panel/` | Project root |
| `app.py` | FastAPI application entry point |
| `ssh_manager.py` | SSH connection manager |
| `awg_manager.py` | WireGuard protocol manager |
| `xray_manager.py` | Xray/VLESS-Reality manager |
| `dns_manager.py` | DNS protocol manager |
| `telemt_manager.py` | TELMT protocol manager |
| `telegram_bot.py` | Telegram bot integration |
| `tests/` | Unit tests |
| `templates/` | Jinja2 web templates |
| `translations/` | i18n JSON files |

## Key Patterns

### Protocol Manager Interface
Each manager follows this pattern:
```python
class XxxManager:
    def __init__(self, ssh_manager): ...
    def check_installed(self): ...
    def install_protocol(self): ...
    def remove_protocol(self): ...
    def get_server_status(self): ...
```

### FastAPI Route Pattern
```python
@router.post("/protocol/action")
async def protocol_action(request: Request, data: ActionModel):
    # auth check
    # delegate to manager
    # return JSONResponse
```

### Docker Command Pattern
```python
out, err, code = self.ssh.run_sudo_command(f"docker {action} {container}")
if code != 0:
    return {"status": "error", "message": err}
```
