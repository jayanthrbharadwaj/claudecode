---
disable-model-invocation: true
---

# /forge:validate

Run the full verification suite — gating reviews plus advisory checks — and produce a consolidated report.

## When to Use

Use this command for a comprehensive quality check before creating a PR or after major implementation work. This runs both the mandatory gating checks and advisory quality checks.

For gating reviews only (faster), use `/forge:review` instead.

## Arguments

None.

## Process

### Tier 1: Gating Checks (all must PASS)

These are mandatory. A FAIL in any gating check blocks PR creation.

1. **Spec Review**
   - Invoke the **spec-reviewer** agent.
   - Compares implementation against spec acceptance criteria.
   - Result: PASS or FAIL with details.

2. **Code Review**
   - Invoke the **code-reviewer** agent.
   - Checks code quality, conventions, performance, and architecture compliance.
   - Result: PASS or FAIL with details.

3. **Security Review**
   - Invoke the **security-reviewer** agent.
   - Checks OWASP Top 10, auth flows, secrets handling, dependency vulnerabilities.
   - Result: PASS or FAIL with details.

### Tier 2: Advisory Checks (informational)

These provide additional quality signals but do not block PR creation.

4. **Test Coverage**
   - Run `make test` with coverage reporting.
   - Check if coverage meets the 80% threshold.
   - Result: coverage percentage and PASS/WARN.

5. **Linter Check**
   - Run `python3 .claude/linters/lint_all.py`.
   - Report any violations found.
   - Result: violation count and PASS/WARN.

6. **Dependency Audit**
   - For Python: check for known vulnerabilities in dependencies (e.g., `pip-audit` or `safety check`).
   - For Node: run `npm audit` or equivalent.
   - Result: vulnerability count and PASS/WARN.

### Consolidated Report

7. Produce a summary report in this format:

```
## Validation Report

### Tier 1: Gating (must pass)
| Check            | Status | Details              |
|------------------|--------|----------------------|
| Spec Review      | PASS   |                      |
| Code Review      | FAIL   | 2 issues found       |
| Security Review  | PASS   |                      |

### Tier 2: Advisory
| Check            | Status | Details              |
|------------------|--------|----------------------|
| Test Coverage    | PASS   | 87%                  |
| Linters          | WARN   | 1 violation          |
| Dependency Audit | PASS   | 0 vulnerabilities    |

### Overall: FAIL (1 gating check failed)
```

8. If any gating check failed, inform the user:
   > "Gating checks failed. Fix the issues above and re-run `/forge:validate`, or use `/forge:review` to run the gating review loop with automatic fix retries."

9. If all gating checks passed, inform the user:
   > "All gating checks passed. Ready for `/forge:create-pr`."
