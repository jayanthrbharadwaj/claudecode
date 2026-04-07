---
description: "Three-dimension alignment check: code-vs-spec, code-vs-architecture, architecture-vs-requirements"
disable-model-invocation: true
---

# Check Alignment

Runs alignment checks across three dimensions to ensure consistency between code, specs, and architecture.

## Dimensions

### 1. Code vs Spec (`code-spec`)

**Agent**: spec-reviewer
**Question**: Does the implementation match the product spec?
**Checks**: Acceptance criteria coverage, API contracts, data models, business rules

### 2. Code vs Architecture (`code-arch`)

**Agent**: architecture-alignment-checker
**Question**: Does the code match the architecture documentation?
**Checks**: Layer placement, dependency direction, module structure, cross-cutting concerns

### 3. Architecture vs Requirements (`arch-prd`)

**Agent**: prd-architecture-checker
**Question**: Do the architecture docs correctly reflect product requirements?
**Checks**: Requirement coverage, scope alignment, data model completeness

## Process

1. **Determine scope** — which dimension(s) to check:
   - `all` (default): Run all 3 dimensions
   - `code-spec`: Run dimension 1 only
   - `code-arch`: Run dimension 2 only
   - `arch-prd`: Run dimension 3 only
2. **Run selected checkers** in parallel (if multiple dimensions)
3. **Collect results** from each dimension
4. **Produce unified report**:

```markdown
# Alignment Report

| Dimension | Verdict | Issues |
|-----------|---------|--------|
| Code vs Spec | ALIGNED | 0 |
| Code vs Architecture | DRIFT | 2 minor |
| Architecture vs Requirements | ALIGNED | 0 |

## Details
[Per-dimension findings]
```

## Rules

- Default to running all 3 dimensions
- Each dimension runs independently — one failing does not skip others
- Report all findings together for a unified view
