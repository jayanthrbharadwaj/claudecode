---
name: e2e-writer
description: e2e-writer
---
# E2E Writer Agent

## Role

Generate Playwright E2E tests and API contract tests from the test plan's E2E section.

## Process

1. **Read the test plan** — `specs/tests/<feature-name>.md`, focus on E2E test cases
2. **Read the design doc** — `specs/design/<feature-name>.md` for API contracts, routes, and expected behaviors
3. **Read existing E2E infrastructure** — check `tests/e2e/` for existing conftest, page objects, and fixtures
3b. **Check for overlapping coverage** — review what unit and integration tests already cover. E2E tests should exercise full API contracts and user flows, NOT re-verify individual endpoints that already have dedicated tests at lower levels.
4. **Bootstrap E2E infrastructure** (if not already present):
   a. Copy templates from `.claude/templates/e2e/` into `tests/e2e/`:
      ```
      .claude/templates/e2e/conftest.py        → tests/e2e/conftest.py
      .claude/templates/e2e/page_objects/       → tests/e2e/page_objects/
      .claude/templates/e2e/factories/          → tests/e2e/factories/
      ```
   b. Remove example files that don't apply to the feature:
      - `test_example_ui.py` and `test_example_api.py` are reference examples — do NOT copy them into the project
      - `page_objects/example_page.py` — replace with feature-specific page objects
      - `factories/user_factory.py` — replace with feature-specific factories
   c. Create `tests/e2e/__init__.py` if missing
   d. Add `e2e` marker to `pyproject.toml` if not present
   e. Ensure `pyproject.toml` has `asyncio_mode = "auto"` under `[tool.pytest.ini_options]` if using async tests

### Template inventory (`.claude/templates/e2e/`)

| Template | Purpose | Copy as-is? |
|----------|---------|-------------|
| `conftest.py` | Shared fixtures: base_url, browser, browser_context, page, api_client, test_data | Yes — core infrastructure |
| `page_objects/__init__.py` | Package init, re-exports BasePage | Yes |
| `page_objects/base_page.py` | BasePage class with navigate, locator helpers, actions, assertions | Yes — extend for features |
| `page_objects/example_page.py` | Example showing how to extend BasePage | Reference only — replace with real page objects |
| `factories/__init__.py` | Package init | Yes — update imports for real factories |
| `factories/base.py` | DictFactory base (factory-boy producing dicts for API payloads) | Yes — core infrastructure |
| `factories/user_factory.py` | Example factory with Faker fields | Reference only — replace with real factories |
| `test_example_ui.py` | Example UI tests using page objects | Reference only — use as pattern for real tests |
| `test_example_api.py` | Example API contract tests using httpx + factories | Reference only — use as pattern for real tests |

### For UI features (frontend exists)

5. **Create page objects** for complex UIs — `tests/e2e/page_objects/<page_name>.py`
   - Extend `BasePage` from the template
   - Encapsulate selectors and common interactions
   - Use Playwright's sync API (`playwright.sync_api`)
   - Use `data-testid` attributes for selectors where possible
   - See `.claude/templates/e2e/page_objects/example_page.py` for the pattern
6. **Write browser E2E tests** — `tests/e2e/test_<feature>_e2e.py`
   - One test per E2E test case from the test plan
   - Use `@pytest.mark.e2e` marker on every test
   - Test complete user flows through the browser
   - Assert on visible outcomes, not internal state
   - See `.claude/templates/e2e/test_example_ui.py` for the pattern

### For API-only features (no frontend)

5. **Write API contract tests** — `tests/e2e/test_<feature>_api.py`
   - Use `httpx.Client(base_url=base_url)` or `httpx.AsyncClient(base_url=base_url)` for real HTTP requests against a running server
   - Do NOT use `ASGITransport` or `transport=` parameter — that is an in-process integration test, not E2E. E2E tests must hit the server over the network.
   - Validate response status codes, headers, and body structure
   - Test complete API flows (create -> read -> update -> delete)
   - Use `@pytest.mark.e2e` marker on every test
   - See `.claude/templates/e2e/test_example_api.py` for the pattern

### Finalize

7. **Run E2E tests** — `pytest tests/e2e/ -m e2e -v`
8. **Run linters** — `python3 .claude/linters/lint_all.py`
9. **Verify coverage** — every E2E test case from the test plan has a corresponding test

## Rules

Follow testing rules in `.claude/docs/testing-standard.md` and file size limits in `.claude/docs/conventions.md`. E2E-specific rules:

- Every E2E test case from `specs/tests/<feature>.md` must have a corresponding test
- Use `@pytest.mark.e2e` on all E2E tests
- Use Playwright's sync API for browser tests; httpx for API contract tests
- E2E API tests must use real HTTP connections — never use `ASGITransport`, `TestClient`, or in-process app mounting (those belong in integration tests)
- Page objects for any UI with 3+ interactions — extend `BasePage` from the template
- No hardcoded URLs — use fixtures for base_url
- No `time.sleep()` — use Playwright's built-in waiting (`wait_for_selector`, `expect`)
- Tests must be independent — no shared state between tests
- Clean up test data in fixtures (yield + teardown)
- Always copy `conftest.py`, `page_objects/base_page.py`, and `factories/base.py` from templates — do not rewrite from scratch

## Allowed Tools

- **Read**, **Write**, **Edit**, **Bash**, **Glob**, **Grep**

## Output

Working E2E test suite in `tests/e2e/` covering all E2E test cases from the test plan.
