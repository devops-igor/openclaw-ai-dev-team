# Python Development Standards

## Code Style

### Formatting — black
- **Always use `black`** with default settings (line-length = 100)
- Run `black .` before every commit
- Do not disable black checks inline unless absolutely necessary

### Linting — flake8
- Max line length: **100** (enforced by project `.flake8`)
- **Ignored rules**: E203, W503, E501, E722, F841
- Run `flake8 .` before every commit

### Type Hints
- **Required** on all public function signatures
- Use `from __future__ import annotations` for forward references
- Prefer `Optional[X]` over `X | None`
- No `Any` in public APIs — only in internals with a comment explaining why

```python
from __future__ import annotations
from typing import Optional

def get_user(user_id: int) -> Optional[dict]:
    ...
```

## Project Structure

### FastAPI Routes
- All routes in `app.py` or a dedicated `routes/` package
- Route handlers delegate to **manager classes** — no business logic in routes
- Use Pydantic models for all request/response validation
- Always inject `Request` and access session/auth via it — never read globals

```python
@router.post("/protocol/action")
async def protocol_action(request: Request, data: ActionModel):
    # auth check first
    if not request.session.get("authenticated"):
        return JSONResponse({"status": "error"}, status_code=401)
    # delegate to manager
    result = await ProtocolManager(data).run()
    return JSONResponse(result)
```

### Manager Classes
- One manager per protocol/domain: `ssh_manager.py`, `awg_manager.py`, `xray_manager.py`
- Each manager takes an `SSHManager` instance in `__init__`
- All Docker/SSH commands go through the manager — never raw `subprocess.run`

## SSH & Docker

### SSH Commands
- **Always use `run_sudo_command`** for Docker, service, and config operations
- **Always use `run_command`** for read-only queries
- Never assemble SSH commands with f-strings from untrusted input — validate all inputs
- Log every command: `logger.info(f"Running: {cmd}")`

### Docker Operations
- Container naming: `amnezia-<protocol>`
- Config path: `/opt/amnezia/<protocol>/`
- Always check `docker ps` output for `"Up"` before assuming a container is running
- Always handle non-zero exit codes — don't assume success

```python
out, err, code = self.ssh.run_sudo_command(f"docker {action} {container}")
if code != 0:
    logger.error(f"Docker command failed: {err}")
    return {"status": "error", "message": err}
```

## Async Patterns

### asyncio
- Every route handler that does I/O should be `async def`
- Always `await` coroutines — never create bare `asyncio.create_task` without storing the Task
- For background asyncio tasks (e.g., Telegram bot), use `asyncio.create_task` and store in a module-level var

### Threading
- Use `asyncio.to_thread()` for blocking sync I/O inside async handlers
- Never block the event loop with long-running sync code

## Error Handling

### Logging
- Use `logger.info()`, `logger.warning()`, `logger.error()` — **never `print()`**
- Include context in log messages: `logger.error(f"Install failed: {err}")`
- Never swallow exceptions silently

```python
# WRONG
try:
    do_something()
except Exception:
    pass

# RIGHT
try:
    do_something()
except SpecificError as e:
    logger.error(f"Failed to do something: {e}")
    return {"status": "error", "message": str(e)}
```

## Security

### No Hardcoded Secrets
- Never put credentials, tokens, or keys in source code
- Use environment variables or a config file read at runtime
- Validate all user input — never trust `request.json()` without Pydantic validation

### Session & Auth
- All protected routes must check `request.session` before proceeding
- Use `secrets.token_hex(32)` for session secret (already set in app.py)
- Never expose internal error details in API responses

### SSH
- Always use sudo commands via the SSHManager — never raw `ssh user@host sudo ...`
- Command injection via shell metacharacters is a critical risk — sanitize all input

## Testing — pytest

### Structure
- Test files in `tests/`, named `test_<module>.py`
- One test class per module: `class TestDnsManager:`
- Use `unittest.mock.MagicMock` for SSH/Docker mocking
- Never make real SSH connections in tests

### Fixtures
```python
def setup_method():
    self.mock_ssh = MagicMock()
    self.dns = DNSManager(self.mock_ssh)
```

### Coverage
- Target **≥80%** coverage
- Cover happy path + error paths + edge cases (empty input, SSH failure, non-zero exit)

## API Design

### Pydantic Models
- Request models: `class ActionModel(BaseModel):`
- Response models: return `JSONResponse` with a dict, or a `BaseModel` with `.model_dump_json()`
- Never return raw dicts from route handlers without type hints

### HTTP Status Codes
- `200` — success
- `400` — bad request (validation error)
- `401` — unauthorized
- `404` — not found
- `500` — internal error

## Jinja2 Templates

- Templates live in `templates/`
- Base template defines the layout; child templates extend it
- No Python logic in templates — only simple `{% if %}` / `{% for %}` loops
- Pass data from routes as dicts, not ORM objects

## Dependencies

- All production deps in `requirements.txt`
- All dev deps in `requirements-dev.txt`
- Run `pip-audit` to check for CVEs before each handoff
- Pin major versions (e.g., `fastapi>=0.100,<1.0`) to avoid surprise breaking changes
