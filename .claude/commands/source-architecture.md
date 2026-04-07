---
disable-model-invocation: true
---

# /forge:source-architecture

Reverse-engineer architecture documentation from existing code.

## When to Use

- You have an existing codebase with no architecture docs
- You want to generate architecture docs that reflect the actual code structure
- You want to discover the implicit architecture of a project

## Arguments

- **scope** (optional): Directory or module to analyze (default: `src/`)

## Process

1. Invoke the `sync-architecture` skill
2. Scan the codebase for:
   a. Module/package structure and boundaries
   b. Import graphs and dependency patterns
   c. Layer identification (data, business logic, presentation)
   d. Cross-cutting patterns (logging, error handling, config)
   e. External dependencies and integration points
3. Generate architecture documentation in `.claude/docs/architecture.md` format
4. Present the generated docs for user review and refinement
