---
disable-model-invocation: true
---

# /forge:check

Run alignment checks across three dimensions: code-vs-spec, code-vs-architecture, architecture-vs-requirements.

## When to Use

- Before creating a PR, to verify everything is aligned
- After significant implementation changes
- When you suspect drift between code, specs, and architecture docs

## Arguments

- **dimension** (optional): `all`, `code-spec`, `code-arch`, `arch-prd` (default: `all`)
- **feature** (optional): Feature name to check (default: auto-detect from current branch)

## Process

1. Invoke the `check-alignment` skill with the specified dimension
2. Run the selected checks:
   a. **code-spec**: Invoke spec-reviewer — does the code match the spec?
   b. **code-arch**: Invoke architecture-alignment-checker — does the code match architecture docs?
   c. **arch-prd**: Invoke prd-architecture-checker — do architecture docs match product requirements?
3. Collect results from all checkers
4. Present a unified alignment report showing:
   - Per-dimension verdict (ALIGNED / MISALIGNED)
   - Specific findings with file references
   - Recommended actions for any misalignments
