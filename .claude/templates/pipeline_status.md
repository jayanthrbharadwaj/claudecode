<!-- AGENT: Do not read during exploration. This template is used only when creating specs. Read .claude/docs/scaffold-overview.md instead. -->
# Pipeline Status: [Feature Name]

**Started**: [timestamp]
**Current Phase**: [phase name]
**Status**: [in_progress | blocked | completed]

## Feature Queue

| # | Feature | Priority | Current Phase | Status |
|---|---------|----------|---------------|--------|
| 1 | [feature name] | P0 | [phase] | [status] |

## Phase Log

| Phase | Started | Agent | Artifacts | Status | Notes |
|-------|---------|-------|-----------|--------|-------|
| 1. Spec | | spec-writer | `specs/app_spec.md` | | |
| 2. Stories | | spec-writer | `specs/stories/<name>.md` | | |
| 3. Design | | spec-writer | `specs/design/<name>.md` | | |
| 4. Test Plan | | spec-writer | `specs/tests/<name>.md` | | |
| 5. Exec Plan | | spec-writer | `specs/plans/<name>.md` | | |
| 6. Approve Plan | | human | — | | |
| 7. Implement | | implementer | `src/`, `tests/` | | |
| 8. Test Fill | | test-writer | `tests/` | | |
| 9. E2E Tests | | e2e-writer | `tests/e2e/` | | |
| 10. DevOps | | devops | `infra/`, `.github/workflows/` | | |
| 11. Review | | spec-reviewer, code-reviewer | review verdicts | | |
| 12. Approve PR | | human | — | | |
| 13. PR | | pr-writer | PR link | | |

## Blocking Issues

| Issue | Blocking Phase | Assigned To | Status |
|-------|---------------|-------------|--------|
| — | — | — | — |

## Team (if applicable)

| Team Name | Stories | Members | Status |
|-----------|---------|---------|--------|
| — | — | — | — |
