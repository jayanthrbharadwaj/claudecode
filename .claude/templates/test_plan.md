<!-- AGENT: Do not read during exploration. This template is used only when creating specs. Read .claude/docs/scaffold-overview.md instead. -->
# Test Plan: [Feature Name]

**Feature Spec**: `specs/features/[feature-name].md`
**User Stories**: `specs/stories/[feature-name].md`
**Created**: [YYYY-MM-DD]

## Test Cases

| ID | Type | Story | Description | Input | Expected Output |
|----|------|-------|-------------|-------|-----------------|
| TC-001 | unit | US-001 | [What is being tested] | [Test input] | [Expected result] |
| TC-002 | integration | US-001 | [What is being tested] | [Test input] | [Expected result] |
| TC-003 | e2e | US-002 | [What is being tested] | [User action] | [Expected behavior] |

## Test Data & Fixtures

| Fixture | Type | Description | Used By |
|---------|------|-------------|---------|
| `valid_example` | dict | A valid example payload | TC-001, TC-002 |
| `invalid_example` | dict | Missing required fields | TC-003 |

## E2E Tests (Playwright)

| Test | Page | Action | Assertion |
|------|------|--------|-----------|
| TC-003 | `/examples` | Click "Create", fill form, submit | New item appears in list |
| TC-004 | `/examples` | Submit empty form | Validation error displayed |

## Dependencies

Stories that must be implemented before these tests can run:

- US-001 (provides the API endpoints)
- US-002 (provides the UI components)

## Coverage Targets

| Scope | Target | Measured By |
|-------|--------|-------------|
| Unit tests | >= 80% line coverage | `pytest --cov` |
| E2E tests | All acceptance criteria | Playwright test results |
| Edge cases | All spec edge cases covered | Manual checklist |
