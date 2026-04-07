# Testing Standard

> Single source of truth for all testing rules. Agents and reviewers reference this file.

## Coverage

- **Minimum: 80%** — enforced by `pytest --cov-fail-under=80`
- Every service function needs a corresponding test
- Every spec acceptance criterion needs at least one test with a spec reference comment

## Test Organization

```
tests/
  types/          # Type validation tests
  config/         # Configuration loading tests
  repo/           # Data access tests (with mocks)
  service/        # Business logic tests (core coverage)
  runtime/        # Integration tests
  ui/             # UI/CLI output tests
  e2e/            # Playwright browser + httpx API contract tests
```

## Test Naming

```
test_<function_name>_<scenario>_<expected_outcome>
```

Examples: `test_create_user_valid_input_returns_user`, `test_create_user_duplicate_email_raises_conflict`

## Fixtures

- Before creating a fixture, check `tests/conftest.py` and `tests/*/conftest.py` for existing ones — reuse first
- If the same fixture setup appears in 2+ test files, extract to the nearest shared `conftest.py`
- Before writing a test, check if an equivalent test already exists — do not duplicate coverage

## Assertions

Every assertion must verify **specific behavior** — exact values, exception types, or state changes.

**Banned (vacuous) patterns:**
- `assert result is not None`
- `assert response` (truthiness only)
- `assert len(items) > 0` without checking contents
- `assert service is not None` (constructor tests)

**Good patterns:**
- `assert result.id == UserId("u-123")`
- `assert result.email == "alice@example.com"`
- `pytest.raises(DuplicateEmailError)`
- `assert response.status_code == 201`

## Async Tests

When writing async tests, ensure `pyproject.toml` has `asyncio_mode = "auto"` under `[tool.pytest.ini_options]`.

## Markers

Use pytest markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.e2e`.

## Mock Strategy Per Layer

| Layer   | Test Type        | Mock Strategy                                  |
|---------|------------------|-------------------------------------------------|
| Types   | Unit             | None (pure data structures)                    |
| Config  | Unit             | Mock environment variables                     |
| Repo    | Unit+Integration | Mock DB (unit), SQLite in-memory (integration) |
| Service | Unit             | Mock repo dependencies                         |
| Runtime | Integration      | TestClient with mocked services                |
| UI      | Integration+E2E  | TestClient (integration), Playwright (E2E)     |

## Type Annotations

All function signatures must have type annotations — including test functions, fixtures, and E2E tests, not just `src/`.
