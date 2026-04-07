---
disable-model-invocation: true
---

# /forge:spec-sync

Bidirectional synchronization between specs and code. Detects drift and generates or updates artifacts to restore alignment.

## When to Use

Use this command when specs and code may have diverged. Common scenarios:
- After manual code changes that were not spec-driven
- When inheriting a codebase that lacks specs
- Periodic audits to ensure spec-code alignment
- After a sprint to verify all acceptance criteria are met

## Arguments

- **direction** (required): The sync direction. Must be one of:
  - `from-code` — Scan code and generate/update specs to match the implementation
  - `from-specs` — Compare spec acceptance criteria against implementation and report drift

Example:
- `/forge:spec-sync from-code`
- `/forge:spec-sync from-specs`

## Process

### Direction: `from-code`

Generate or update specs based on existing code.

1. Scan `src/` to discover all modules, their layers, and their responsibilities.
2. For each service-layer module, identify:
   - Public API surface (functions, classes, methods)
   - Domain types used
   - Dependencies (which repo/config modules it uses)
   - Error handling patterns
   - Business rules encoded in the logic
3. Check for existing specs in `specs/features/`:
   - If a spec exists for a module, compare the spec's acceptance criteria against the code. Update the spec with any new functionality found in the code.
   - If no spec exists, generate a new feature spec from the code patterns.
4. Check for existing stories in `specs/stories/`:
   - If stories exist, verify they cover the functionality found in code.
   - Generate new stories for unmatched functionality.
5. Output:
   - New or updated files in `specs/features/` and `specs/stories/`
   - A sync report listing what was generated or updated

### Direction: `from-specs`

Compare specs against code and report drift.

1. Read all specs from `specs/features/` and extract acceptance criteria.
2. Read all stories from `specs/stories/` and extract requirements.
3. For each acceptance criterion and requirement:
   a. Search `src/` for the implementing code.
   b. Search `tests/` for covering tests.
   c. Classify as:
      - **Implemented + Tested**: criterion is met with test coverage
      - **Implemented + Untested**: code exists but no test covers the criterion
      - **Not Implemented**: no code found matching the criterion
      - **Partially Implemented**: code exists but does not fully meet the criterion
4. Output a drift report:

```
## Spec-Code Drift Report

### Feature: User Authentication (specs/features/auth_spec.md)
| Criterion                        | Status               | Location            |
|----------------------------------|----------------------|---------------------|
| Users can register with email    | Implemented + Tested | src/service/auth.py |
| Password reset via email         | Not Implemented      | —                   |
| Session timeout after 30min      | Partially Implemented| src/runtime/auth.py |

### Summary
- Implemented + Tested: 8/12 (67%)
- Implemented + Untested: 2/12 (17%)
- Not Implemented: 1/12 (8%)
- Partially Implemented: 1/12 (8%)
```

5. If drift is significant, suggest next steps:
   - For unimplemented criteria: suggest `/forge:work-on-next` or `/forge:add-feature`
   - For untested criteria: suggest running test-writer agent
   - For partial implementations: flag specific gaps for the user to review
