---
disable-model-invocation: true
---

# /forge:debug

Systematic 5-phase debugging process. Describe the bug and the debug agent takes over with a structured approach.

## When to Use

Use this command when you encounter a bug that needs methodical investigation. This is particularly useful for:
- Bugs that are hard to reproduce
- Regressions after recent changes
- Issues that span multiple layers of the architecture
- Bugs where the root cause is unclear

## Arguments

- **description** (required): A description of the bug. Include any error messages, stack traces, or reproduction steps you have. Everything after `/forge:debug` is treated as the bug description.

Example: `/forge:debug user registration returns 500 error when email contains a plus sign`

## Process

### Phase 1: Reproduce
1. Analyze the bug description provided by the user.
2. Identify the relevant code paths by searching `src/` and `tests/`.
3. Attempt to reproduce the bug:
   - Look for an existing test that covers the scenario. If found, run it to confirm failure.
   - If no existing test, write a minimal reproduction test that demonstrates the bug.
4. Confirm the bug is reproducible. If it cannot be reproduced, report findings and ask the user for more information.

### Phase 2: Bisect
5. Identify the scope of the bug — which layers and modules are involved.
6. Use git log to check recent changes to affected files.
7. Narrow down the root cause location:
   - Check inputs and outputs at each layer boundary.
   - Add targeted assertions or logging to isolate where behavior diverges from expectations.

### Phase 3: Hypothesize
8. Form a hypothesis about the root cause based on bisection findings.
9. Present the hypothesis to the user:
   > "Root cause hypothesis: [description]. The issue appears to be in [file:line] where [explanation]."
10. Verify the hypothesis by checking the code path and confirming the failure mechanism.

### Phase 4: Fix
11. Implement the fix in the identified location.
12. Follow the 6-layer architecture — ensure the fix is in the correct layer.
13. Run `python3 .claude/linters/lint_all.py` to verify the fix complies with linters.
14. Run `make test` to verify existing tests still pass.

### Phase 5: Regression Test
15. Write or update a test that specifically covers the bug scenario.
16. The test must:
    - Fail without the fix (verify by mentally tracing the old code path).
    - Pass with the fix.
    - Cover edge cases related to the bug.
17. Run `make test` to confirm the new test passes along with all existing tests.

### Report
18. Summarize the debugging session:
    - **Bug**: What was reported
    - **Root cause**: What was found
    - **Fix**: What was changed (with file paths and line numbers)
    - **Regression test**: What test was added
    - **Confidence**: How confident the fix is (based on test coverage of the scenario)
