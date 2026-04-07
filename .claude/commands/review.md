---
disable-model-invocation: true
---

# /forge:review

Run the 3-stage gating review with automatic fix-and-retry loops. All three stages must pass before a PR can be created.

## When to Use

Use this command after implementation is complete and before creating a PR. This runs only the gating reviews (Tier 1) with automatic retry — if a review fails, the implementer is re-invoked to fix issues, then the review runs again (max 3 cycles per stage).

For a full validation including advisory checks, use `/forge:validate` instead.

## Arguments

None.

## Process

### Stage 1: Spec Review

1. Invoke the **spec-reviewer** agent.
2. The spec-reviewer compares the implementation against the spec acceptance criteria in `specs/features/` and story requirements in `specs/stories/`.
3. If **PASS**: proceed to Stage 2.
4. If **FAIL**:
   a. Log the failures.
   b. Re-invoke the **implementer** agent with the specific failures to fix.
   c. Run `python3 .claude/linters/lint_all.py` and `make test` after fixes.
   d. Re-invoke the **spec-reviewer** agent.
   e. Repeat up to **3 cycles**. If still failing after 3 cycles, report the persistent failures and stop.

### Stage 2: Code Review

5. Invoke the **code-reviewer** agent.
6. The code-reviewer checks code quality, naming conventions, architecture layer compliance, file size limits, and performance concerns.
7. If **PASS**: proceed to Stage 3.
8. If **FAIL**:
   a. Log the failures.
   b. Re-invoke the **implementer** agent with the specific failures to fix.
   c. Run `python3 .claude/linters/lint_all.py` and `make test` after fixes.
   d. Re-invoke the **code-reviewer** agent.
   e. Repeat up to **3 cycles**. If still failing after 3 cycles, report and stop.

### Stage 3: Security Review

9. Invoke the **security-reviewer** agent.
10. The security-reviewer checks OWASP Top 10, authentication/authorization flows, secrets handling, input validation, and dependency vulnerabilities.
11. If **PASS**: all stages complete.
12. If **FAIL**:
    a. Log the failures.
    b. Re-invoke the **implementer** agent with the specific failures to fix.
    c. Run `python3 .claude/linters/lint_all.py` and `make test` after fixes.
    d. Re-invoke the **security-reviewer** agent.
    e. Repeat up to **3 cycles**. If still failing after 3 cycles, report and stop.

### Final Report

13. Report the result of each stage:
    ```
    ## Review Results
    | Stage           | Status | Cycles | Details           |
    |-----------------|--------|--------|-------------------|
    | Spec Review     | PASS   | 1      |                   |
    | Code Review     | PASS   | 2      | Fixed on retry    |
    | Security Review | PASS   | 1      |                   |
    ```

14. If **all three stages PASS**:
    > "All reviews passed. Ready for `/forge:create-pr`."

15. If **any stage failed after 3 cycles**:
    > "Review failed after max retries. Manual intervention required for the issues listed above."
