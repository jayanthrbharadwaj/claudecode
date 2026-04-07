---
disable-model-invocation: true
---

# /forge:design-architecture

Design or update the project's architecture documentation.

## When to Use

- Starting a new project and need architecture docs
- Refactoring the architecture and need to update docs
- Validating that existing architecture docs match the codebase

## Arguments

- **action** (optional): `create`, `update`, or `validate` (default: `create`)

## Process

1. Invoke the `architecture` skill with the specified action
2. **create**: Analyze codebase structure, generate `.claude/docs/architecture.md` covering layers, dependencies, cross-cutting concerns
3. **update**: Read existing architecture docs, scan codebase for deviations, update docs to reflect current state
4. **validate**: Run architecture-alignment-checker agent against current code and docs, report findings
5. Present results to the user for review
