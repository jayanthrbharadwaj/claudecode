---
description: "Architecture documentation management: create, update, and validate architecture docs"
disable-model-invocation: true
---

# Architecture

Manages the project's architecture documentation lifecycle.

## Actions

### create

Generate architecture docs from scratch:

1. Scan `src/` for module structure, imports, and patterns
2. Identify layers and their boundaries
3. Map dependency graph between modules
4. Document cross-cutting concerns (logging, error handling, config)
5. Generate `.claude/docs/architecture.md` in the standard format:
   - Layer model diagram
   - Dependency rules table
   - Module descriptions
   - Cross-cutting concerns
   - Key constraints

### update

Update existing architecture docs to match code:

1. Read current `.claude/docs/architecture.md`
2. Scan `src/` for changes since last update
3. Identify new modules, changed boundaries, new dependencies
4. Update the docs to reflect current state
5. Highlight what changed for user review

### validate

Check code-vs-architecture alignment:

1. Invoke the architecture-alignment-checker agent
2. Present findings: ALIGNED, DRIFT, or VIOLATION
3. For DRIFT findings, suggest updating either code or docs

## Rules

- Architecture docs must always be kept in sync with code
- Validation runs the actual linter (`python3 .claude/linters/layer_deps.py`)
- Never invent architecture that doesn't exist in code (for create/update actions)
