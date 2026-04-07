---
description: "Bidirectional spec-to-code synchronization engine for drift detection"
disable-model-invocation: true
---

# Spec Sync Engine

Bidirectional synchronization between specs in `specs/` and implementation in `src/`. Detects drift in both directions and generates reports or updates.

## Directions

### from-code: Discover specs from implementation

Scans the codebase and generates or updates specs to match what is actually implemented.

**Process**:

1. **Scan source code** using a research agent (Task tool with subagent_type Explore):
   - Scan `src/types/` for Pydantic models -> extract type specs
   - Scan `src/ui/` for route handlers -> extract API endpoint specs
   - Scan `src/service/` for service functions -> extract business rule specs
   - Scan `tests/` for test assertions -> extract acceptance criteria

2. **Map discovered components to specs**:
   For each discovered component, search `specs/features/` for a matching spec file.

3. **Report unmatched code**:
   Components in `src/` that have no corresponding spec in `specs/features/`.

4. **Generate or update specs**:
   For each unmatched component, generate a feature spec using `.claude/templates/feature_spec_lite.md` as the template. Pre-fill:
   - Summary from docstrings and function signatures
   - Data model from Pydantic models
   - API endpoints from route decorators
   - Business rules from service function logic
   - Acceptance criteria from existing test assertions

5. **Output**: Report at `specs/sync_report.md` listing:
   - Matched: spec + code aligned
   - Code without spec: implementation exists, no spec
   - Generated specs: new specs created from code

### from-specs: Verify implementation matches specs

Scans all specs and verifies that each requirement has corresponding implementation and tests.

**Process**:

1. **Read all specs** from `specs/features/*.md`

2. **For each acceptance criterion** in each spec:
   - Search `src/` for matching implementation (by function name, route path, or business rule)
   - Search `tests/` for matching test (by test name or assertion content)

3. **Classify each criterion**:
   - **Implemented + Tested**: code exists AND test exists
   - **Implemented, Untested**: code exists but no test covers this criterion
   - **Unimplemented**: no matching code found
   - **Tested, Not in Spec**: test exists for behavior not in any spec (spec may be outdated)

4. **Output**: Drift report at `specs/sync_report.md` with:
   - Per-feature summary table
   - Detailed listings of unimplemented criteria
   - Detailed listings of untested criteria
   - Suggestions for next actions

## Drift Report Format

```markdown
# Spec Sync Report
Generated: <timestamp>

## Summary
| Feature | Criteria | Implemented | Tested | Drift |
|---------|----------|-------------|--------|-------|
| auth    | 8        | 7           | 6      | 2     |
| search  | 5        | 5           | 3      | 2     |

## Unimplemented Criteria
### auth
- AC-4: "User can reset password via email link" -- no matching code in src/service/

## Untested Criteria
### auth
- AC-3: "Invalid token returns 401" -- implemented in src/ui/auth_routes.py:45 but no test

## Code Without Specs
- src/service/analytics_service.py -- no matching spec in specs/features/
```

## Usage

This skill is invoked by:
- `/forge:sync from-code` -- generate specs from code
- `/forge:sync from-specs` -- verify code matches specs
- `/forge:sync` (no argument) -- run both directions and produce a combined report

## When to Use

- After manual code changes that may have diverged from specs
- Before starting a new feature, to ensure existing specs are up to date
- During review, to verify spec compliance
- Periodically as a health check on spec-code alignment
