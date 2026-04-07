---
description: "TDD enforcement: Iron Law cycle of failing test, minimum code, refactor for every acceptance criterion"
disable-model-invocation: true
---

# Test-Driven Development

The Iron Law of TDD: **Never write production code without a failing test first.**

## The TDD Cycle

For every acceptance criterion in a story:

### RED — Write a Failing Test

1. Write a test that asserts the expected behavior from the acceptance criterion
2. The test MUST fail when run — if it passes, either:
   a. The behavior already exists (skip to next criterion)
   b. The test is wrong (fix the test)
3. The test must fail for the **right reason** — not import errors, syntax errors, or missing fixtures
4. Run: `pytest tests/<test_file>::<test_function> -x -q`
5. Confirm: test fails with an assertion error or expected exception

### GREEN — Write Minimum Code

1. Write the **minimum** production code to make the failing test pass
2. Do NOT write code for other criteria, future needs, or "nice to have" features
3. Do NOT refactor yet — just make the test pass
4. Run: `pytest tests/<test_file>::<test_function> -x -q`
5. Confirm: test passes

### REFACTOR — Clean Up

1. Look for duplication introduced by the new code
2. Improve naming, extract helpers if needed
3. Ensure the code follows project conventions (layers, imports, logging)
4. Run: `pytest tests/ -x -q` (full suite — catch regressions)
5. Confirm: all tests still pass

## When to Use

This skill is automatically applied by:
- The `task-executor` agent for every task
- The `implementer` agent during story implementation
- The `build-unplanned-feature` skill for quick features
- The `execute-task` skill for individual task execution

## Rules

- NEVER skip the RED phase — untested code is unverified code
- NEVER write production code before the test fails
- Each acceptance criterion gets its own RED-GREEN-REFACTOR cycle
- Tests must be meaningful — no vacuous assertions (`assert result is not None`)
- Keep the GREEN phase minimal — only enough code to pass the current test
- The REFACTOR phase must not change behavior — only structure
