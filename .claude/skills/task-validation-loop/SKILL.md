---
description: "Post-task validation with 3 checkers: architecture-alignment, design-consistency, prd-architecture"
disable-model-invocation: true
---

# Task Validation Loop

Lightweight validation that runs after each individual task/story is implemented. Uses 3 focused checkers rather than the full 8-reviewer validation loop.

## Checkers (3)

| # | Agent | Checks |
|---|-------|--------|
| 1 | architecture-alignment-checker | Code matches architecture docs, layer rules respected |
| 2 | design-consistency-checker | UI changes follow design system (skip if no UI changes) |
| 3 | prd-architecture-checker | Architecture docs still match product requirements |

## Process

1. **Detect scope** — identify which files were changed in the current task
2. **Run checkers in parallel**:
   - architecture-alignment-checker: always runs
   - design-consistency-checker: runs only if files in `src/ui/` or template directories were changed
   - prd-architecture-checker: always runs
3. **Collect results** — all 3 must pass (ALIGNED/CONSISTENT)
4. **If any checker fails**:
   a. Present findings to the implementer/task-executor
   b. Fix the issues
   c. Re-run only the failing checker(s)
   d. Max 3 cycles
5. **If still failing after 3 cycles**: log the issues and continue — do not block story progress. The full validation-loop in Phase 10 will catch remaining issues.

## When to Use

Invoked automatically by:
- `task-executor` agent after completing each task
- `implementer` agent after completing each story (when TDD enforcement is active)
- `execute-task` skill after task completion

## Rules

- All 3 checkers must pass for the task to be considered validated
- Skip design-consistency-checker if no UI changes were made
- Max 3 retry cycles — then continue with a warning
- This is a lightweight check — the full validation-loop runs later in Phase 10
