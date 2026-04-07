---
description: "Quick feature implementation without full spec ceremony: TDD + lightweight validation only"
disable-model-invocation: true
---

# Build Unplanned Feature

Builds a feature without the full 11-phase SDLC pipeline. Uses a lightweight brief instead of a full spec, and applies TDD + reduced validation.

## Process

### 1. Parse Request

Invoke the `understanding-feature-requests` skill to parse the user's natural-language request into a structured brief:
- Feature name
- Core requirements (what it must do)
- Acceptance criteria (how to verify)
- Affected layers (which parts of the codebase)
- Constraints (what to avoid)

### 2. Implement with TDD

For each acceptance criterion:
1. **RED**: Write a failing test
2. **GREEN**: Write minimum code to pass
3. **REFACTOR**: Clean up
4. Run tests after each cycle

### 3. Quick Validation

Run the task-validation-loop (3 checkers):
- architecture-alignment-checker
- design-consistency-checker (if UI changes)
- prd-architecture-checker

### 4. Finalize

1. Run full test suite: `pytest tests/ --cov=src --cov-fail-under=80`
2. Run linters: `python3 .claude/linters/lint_all.py`
3. Commit with descriptive message
4. Present results to user

## Rules

- No spec files are created (unless the feature is complex enough to warrant one)
- TDD is still mandatory — no shortcuts
- Quick validation runs but uses the 3-checker loop, not the full 8-reviewer loop
- If validation fails 3 times, suggest running the full pipeline instead
