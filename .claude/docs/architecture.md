# Architecture Reference

## Problem & Scope

This project is a production scaffold for building spec-driven applications with Claude Code agents.
It provides a layered architecture that agents can navigate predictably, with mechanical enforcement
of invariants via linters and hooks. The scaffold is technology-agnostic in the layers above Types,
but ships with Python/FastAPI defaults.

> Code may only depend **forward** through layers.
> Backward dependencies are forbidden and enforced by `.claude/linters/layer_deps.py`.

## Layer Diagram

```
┌─────────────────────────────────────────────┐
│                  UI Layer                   │
│          src/ui/  (presentation)            │
├─────────────────────────────────────────────┤
│               Runtime Layer                 │
│     src/runtime/  (server bootstrap)        │
├─────────────────────────────────────────────┤
│               Service Layer                 │
│    src/service/  (business logic)           │
├─────────────────────────────────────────────┤
│                Repo Layer                   │
│      src/repo/  (data access)              │
├─────────────────────────────────────────────┤
│               Config Layer                  │
│    src/config/  (configuration)             │
├─────────────────────────────────────────────┤
│               Types Layer                   │
│     src/types/  (shared types)              │
└─────────────────────────────────────────────┘
      ▲ Dependency direction: upward only ▲
```

## Dependency Rules

| Layer   | May Import From                       | Must NOT Import From        |
|---------|---------------------------------------|-----------------------------|
| Types   | (none — foundation layer)             | Config, Repo, Service, Runtime, UI |
| Config  | Types                                 | Repo, Service, Runtime, UI  |
| Repo    | Types, Config                         | Service, Runtime, UI        |
| Service | Types, Config, Repo                   | Runtime, UI                 |
| Runtime | Types, Config, Repo, Service          | UI                          |
| UI      | Types, Config, Repo, Service, Runtime | (may import all)            |

## Layer Details

### Types (`src/types/`)
Shared types, enums, constants, Pydantic schemas. No project imports allowed — standard library only.

### Config (`src/config/`)
Configuration loading, environment variable parsing, `BaseSettings` classes. May import from Types.

### Repo (`src/repo/`)
Data access, database queries, external API clients, file I/O. All I/O lives here. May import from Types, Config.

### Service (`src/service/`)
Business logic, orchestration, domain rules. No direct I/O — delegates to Repo. May import from Types, Config, Repo.

### Runtime (`src/runtime/`)
Server bootstrap, middleware registration, dependency injection, lifecycle hooks. May import from all lower layers.

### UI (`src/ui/`)
Presentation layer: FastAPI route handlers, CLI commands, response formatters. May import from all layers.

## Intentional Constraints

These are deliberate architectural decisions, not oversights:

- **Service has no direct I/O** — all database, HTTP, and filesystem access goes through Repo. Service operates on types only.
- **Types has no project imports** — it depends on the standard library and Pydantic only. This keeps it the stable foundation.
- **No global mutable state** — configuration is loaded once in Config and injected forward. No module-level singletons.
- **No cross-layer type definitions** — a type used by multiple layers must live in Types, not defined inline.
- **No raw primitives for domain concepts** — use refined Pydantic types (e.g., `UserId`, `Email`) instead of bare `str` or `int`. This makes code self-documenting for agents and enforces validation at parse boundaries.

## Cross-Cutting Concerns

### Logging
Every module uses structured logging: `import logging; logger = logging.getLogger(__name__)`. Never use `print()`.

### Error Handling
All external calls (API, DB, filesystem) wrapped in try/except in the Repo layer. Catch specific exceptions.

### Authentication
Auth types in Types, validation logic in Service, middleware in Runtime, route guards in UI.

## Why These Constraints?

> "While these rules might feel pedantic or constraining in a human-first workflow,
> with agents they become multipliers: once encoded, they apply everywhere at once."

Constraints allow speed without decay. When agents can rely on a consistent, enforced
structure, they can reason about the full business domain directly from the repository.

## Testing Strategy Per Layer

See `.claude/docs/testing-standard.md` for the full mock strategy table, test organization, fixture rules, and assertion standards.
