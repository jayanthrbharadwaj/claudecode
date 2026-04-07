---
description: "Coding conventions: naming, logging, file size, type hints, import ordering, error handling, code style"
disable-model-invocation: true
---

# Coding Conventions

Standards for naming, logging, file size, type safety, and code organization. These apply to all code in `src/` and `tests/`.

## Naming

### Python
| Element | Convention | Example |
|---------|-----------|---------|
| Files/modules | `snake_case` | `user_service.py` |
| Functions/methods | `snake_case` | `create_user()` |
| Classes/types | `PascalCase` | `UserService`, `CreateUserRequest` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Private members | leading underscore | `_validate_email()` |

### TypeScript
| Element | Convention | Example |
|---------|-----------|---------|
| Files/modules | `camelCase` or `kebab-case` | `userService.ts` |
| Functions | `camelCase` | `createUser()` |
| Components | `PascalCase` | `UserProfile` |
| Types/interfaces | `PascalCase` | `CreateUserRequest` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |

## Type Hints

Required on ALL function signatures, including:
- Production code in `src/`
- Test functions in `tests/`
- Fixtures and helpers

```python
# Good
def create_user(email: Email, name: str) -> User:
    ...

def test_create_user_valid_input(user_repo: MockUserRepo) -> None:
    ...

# Bad -- missing type hints
def create_user(email, name):
    ...
```

**No `Any` type** -- if you need a generic type, use `TypeVar`, `Protocol`, or a union. `Any` defeats the purpose of type checking.

## Structured Logging

All modules must use structured logging. Never use `print()`.

```python
import logging

logger = logging.getLogger(__name__)

# Good
logger.info("user_created", extra={"user_id": user.id, "email": user.email})
logger.error("payment_failed", extra={"order_id": order.id, "reason": str(e)})

# Bad
print(f"Created user {user.id}")
logger.info(f"Created user {user.id}")  # Also bad: unstructured message
```

### Log Levels
| Level | When to Use |
|-------|------------|
| `DEBUG` | Detailed diagnostic info (not in production) |
| `INFO` | Normal operations: requests, state changes |
| `WARNING` | Unexpected but handled: retries, fallbacks |
| `ERROR` | Failed operations that need attention |
| `CRITICAL` | System-level failures requiring immediate action |

## Error Handling

### Rules
1. Catch **specific exceptions**, never bare `except:` or `except Exception:`
2. Log context with every caught exception
3. Define custom exception classes in `src/types/` for domain errors
4. Raise domain exceptions from Service, catch in UI
5. Wrap external exceptions in Repo (e.g., `httpx.HTTPError` -> `ExternalServiceError`)

```python
# Good
class DuplicateEmailError(DomainError):
    def __init__(self, email: Email) -> None:
        super().__init__(f"Email already registered: {email}")
        self.email = email

# In service
def create_user(self, email: Email) -> User:
    if self.user_repo.exists_by_email(email):
        raise DuplicateEmailError(email)
    return self.user_repo.create(email)

# In UI route handler
try:
    user = user_service.create_user(email)
except DuplicateEmailError as e:
    logger.warning("duplicate_email", extra={"email": str(e.email)})
    raise HTTPException(status_code=409, detail=str(e))
```

### Anti-Patterns
- Catching and silently ignoring exceptions
- Catching `Exception` when you know the specific type
- Raising generic `ValueError` or `RuntimeError` for domain errors
- Logging without context (`logger.error("something failed")`)

## File Size Limits

| Metric | Limit |
|--------|-------|
| Lines per file | **300 max** |
| Lines per function | **50 max** |

Enforced by `.claude/linters/file_size.py`. When a file exceeds 300 lines, split it. When a function exceeds 50 lines, extract helper functions or simplify logic.

## Import Ordering

Imports must be ordered in three groups, separated by blank lines:

```python
# 1. Standard library
import logging
from datetime import datetime
from typing import Optional

# 2. Third-party packages
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# 3. Project imports (in layer order: types -> config -> repo -> service -> runtime)
from src.types.user import User, UserId
from src.config.settings import Settings
from src.repo.user_repo import UserRepo
```

## Secrets

- **Never hardcode** secrets, API keys, tokens, or passwords
- All secrets must come from environment variables, loaded via `src/config/`
- Use `.env.example` to document required environment variables (without real values)
- Never commit `.env` files -- ensure `.gitignore` includes them

## Pydantic Types

Use refined Pydantic types for all domain concepts:

```python
# Good -- self-documenting, validated
class UserId(str):
    """Unique user identifier."""

class Email(str):
    """Validated email address."""

# Bad -- raw primitives
user_id: str  # What kind of string? No validation.
email: str    # Could be anything.
```

## Test Conventions

- Naming: `test_<function>_<scenario>_<expected_outcome>`
- All test functions must have type annotations
- Reuse fixtures from `conftest.py` -- check before creating new ones
- No vacuous assertions (`assert result is not None`)
- Every assertion must verify specific behavior: exact values, exception types, or state changes

## Enforcement

These conventions are checked by:
- `.claude/linters/file_size.py` -- file and function size limits
- `.claude/linters/layer_deps.py` -- import ordering within project imports
- Code review agent -- naming, logging, type hints, error handling
- Security review agent -- secrets, input validation
