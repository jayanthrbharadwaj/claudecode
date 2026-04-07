---
disable-model-invocation: true
---

# /forge:source-specs

Reverse-engineer specs from existing code using the spec-sync engine.

## When to Use

- You have an existing codebase with no specs
- You want to generate specs that match the current implementation
- You want to bootstrap the spec-first workflow for an existing project

## Arguments

- **scope** (optional): Feature or module to analyze (default: all)

## Process

1. Invoke the `spec-sync-engine` skill in reverse-engineer mode
2. Analyze the codebase using the research-agent
3. For each identified feature:
   a. Generate a feature spec in `specs/features/` format
   b. Extract user stories from existing code behavior
   c. Document current API contracts and data models
4. Save generated specs to `specs/` directories
5. Present specs for user review and refinement
