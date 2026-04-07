---
description: "Reverse-engineer architecture documentation from existing codebase"
disable-model-invocation: true
---

# Sync Architecture

Reverse-engineers architecture documentation by analyzing the existing codebase structure.

## Process

1. **Scan the codebase**:
   a. Map all packages and modules in `src/`
   b. Build an import dependency graph
   c. Identify layer boundaries (where do Types end and Config begin?)
   d. Find cross-cutting patterns (logging, error handling, config injection)
   e. Identify external integrations (databases, APIs, message queues)

2. **Classify into layers**:
   a. Types: modules with only Pydantic models and no project imports
   b. Config: modules that load configuration
   c. Repo: modules with I/O (database, HTTP, filesystem)
   d. Service: modules with business logic, no direct I/O
   e. Runtime: modules that wire things together
   f. UI: modules with HTTP handlers, CLI commands

3. **Generate architecture document**:
   - Layer model with actual module paths
   - Dependency graph (what imports what)
   - Cross-cutting concerns
   - Key constraints derived from code patterns
   - Deviations from the ideal 6-layer model (if any)

4. **Write to `.claude/docs/architecture.md`** or present for review

## Rules

- Only document what actually exists — do not prescribe ideal architecture
- Flag deviations from the 6-layer model but do not fix them (that's the refactorer's job)
- Include the import graph as evidence for layer classification
