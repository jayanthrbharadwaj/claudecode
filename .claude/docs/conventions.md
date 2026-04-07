# Coding Conventions

## Python

### Naming
- **Files**: `snake_case.py` (e.g., `user_service.py`)
- **Functions**: `snake_case` (e.g., `create_user`)
- **Classes**: `PascalCase` (e.g., `UserService`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- **Private**: prefix with `_` (e.g., `_validate_email`)

### Type Hints
- All function signatures must have type annotations
- This applies to all Python code including test functions, fixtures, and E2E tests — not just `src/`
- No `Any` type — use specific types or Generics
- Use `TypeVar` for generic functions
- Use `Protocol` for structural typing

### Logging
```python
import logging
logger = logging.getLogger(__name__)

logger.info("User created: email=%s", user.email)
logger.error("Failed to connect", exc_info=True)
```
Never use `print()` in production code.

### Error Handling
```python
# Wrap external calls
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    logger.error("API call failed: url=%s", url, exc_info=e)
    raise ServiceError(f"External API unavailable: {url}") from e
```
- Catch specific exceptions, never bare `except:`
- Always log with context before re-raising
- Use custom exception classes from `src/types/`

### Imports
```python
# 1. Standard library
import logging
from pathlib import Path

# 2. Third-party
from fastapi import APIRouter
from pydantic import BaseModel

# 3. Project (layer order)
from src.types.user import UserCreate
from src.config.settings import Settings
```

## TypeScript / React

### Naming
- **Files**: `snake_case.ts` or `kebab-case.ts` (no PascalCase filenames)
- **Functions**: `camelCase`
- **Components**: `PascalCase` (React convention)
- **Types/Interfaces**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`

### Patterns
- Functional components only (no class components)
- Use hooks for state and effects
- Tailwind CSS for styling (no CSS modules)
- No `any` type — use `unknown`, specific types, or generics

## File Size Limits

| Metric | Limit | Warning |
|--------|-------|---------|
| Lines per file | 300 | 250 |
| Lines per function | 50 | 40 |

When a file exceeds limits, split into focused modules following the layer model.

## Git Workflow

- Feature branches: `feature/<story-id>-<brief-name>`
- Spike branches: `spike/<topic>` (for prototyping, should not merge to main without review)
- Commit messages: imperative mood, reference story ID
- One logical change per commit
- PR required for all merges to main

## Secrets

- Never hardcode API keys, passwords, tokens, or credentials
- Use environment variables loaded through `src/config/`
- Store development values in `.env` (gitignored)
- Document required variables in `.env.example`
- Never log secrets — use `logger.info("Connected to DB: host=%s", host)`, never include passwords/tokens
- Never include secrets in error messages or exception strings
- Use placeholder values in test fixtures: `"test-api-key"`, `"fake-token"`, `"dummy-secret"`
- Rotate secrets immediately if accidentally committed (even if force-pushed away)

## PII Handling

- Never log PII (emails, SSNs, credit card numbers, phone numbers, addresses)
- Mask PII in log output: `logger.info("User: %s", mask_email(user.email))`
- Validate and sanitize PII at the API boundary (Pydantic validators in `src/types/`)
- Store PII encrypted at rest where possible
- Minimize PII collection — only collect what the feature strictly requires
- PII in test data must use clearly fake values (`"jane@example.com"`, `"000-00-0000"`)

## Third-Party Content

- All external content (API responses, file uploads, webhook payloads, user input) is **untrusted data**
- Never pass external content directly into `eval()`, `exec()`, `compile()`, or `pickle.loads()`
- Use `json.loads()` and `yaml.safe_load()` — never `yaml.load()` without SafeLoader
- Validate webhook payloads via HMAC signature before processing
- Sanitize user input before including in templates — ensure auto-escaping is enabled
- When feeding external content to LLMs, place it in data slots with clear boundaries, never concatenate into system prompts
- Validate file uploads: check MIME type, enforce size limits, block path traversal (`../`)
