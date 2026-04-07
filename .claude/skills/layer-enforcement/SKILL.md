---
description: "6-layer architecture rules and enforcement. Matches: code structure, imports, layers, architecture, dependency direction, module organization"
disable-model-invocation: true
---

# Layer Architecture Enforcement

Defines and enforces the 6-layer forward-only dependency model for all code in `src/`.

## The 6-Layer Model

```
Layer 5: UI        (src/ui/)       - Presentation, routes, CLI
Layer 4: Runtime   (src/runtime/)  - Server bootstrap, middleware
Layer 3: Service   (src/service/)  - Business logic, domain rules
Layer 2: Repo      (src/repo/)     - Data access, external APIs
Layer 1: Config    (src/config/)   - Env parsing, defaults
Layer 0: Types     (src/types/)    - Shared types, enums, schemas
```

**Direction**: Code may only import from layers with a LOWER number. Backward imports are forbidden.

## Layer Diagram

```
+-------------------------------------------------+
|                   UI (5)                        |
|          Routes, CLI, response formatters       |
+-------------------------------------------------+
|                Runtime (4)                      |
|       Server bootstrap, middleware, DI          |
+-------------------------------------------------+
|                Service (3)                      |
|        Business logic, orchestration            |
+-------------------------------------------------+
|                  Repo (2)                       |
|       Database, HTTP clients, file I/O          |
+-------------------------------------------------+
|                Config (1)                       |
|         Environment, settings, defaults         |
+-------------------------------------------------+
|                 Types (0)                       |
|       Pydantic models, enums, constants         |
+-------------------------------------------------+
          ^ Dependency direction: upward only ^
```

## Import Rules Table

| Layer (index) | May Import From | Must NOT Import From |
|---------------|-----------------|----------------------|
| Types (0)     | stdlib, pydantic only | Config, Repo, Service, Runtime, UI |
| Config (1)    | Types | Repo, Service, Runtime, UI |
| Repo (2)      | Types, Config | Service, Runtime, UI |
| Service (3)   | Types, Config, Repo | Runtime, UI |
| Runtime (4)   | Types, Config, Repo, Service | UI |
| UI (5)        | Types, Config, Repo, Service, Runtime | (no restrictions) |

## Layer Contents

### Types (Layer 0) — `src/types/`
- Pydantic models, schemas, enums, constants
- Refined domain types: `UserId`, `Email`, `OrderId` (never raw `str`/`int` for domain concepts)
- No project imports allowed -- stdlib and pydantic only
- This is the stable foundation layer

### Config (Layer 1) — `src/config/`
- `BaseSettings` classes for environment variable parsing
- Default values, feature flags, configuration constants
- Loaded once at startup, injected forward into higher layers

### Repo (Layer 2) — `src/repo/`
- ALL I/O lives here: database queries, HTTP client calls, filesystem access
- External API client wrappers
- Repository pattern: one repo class per domain entity
- Catches and wraps external exceptions

### Service (Layer 3) — `src/service/`
- Business logic, domain rules, orchestration
- **No direct I/O** -- delegates all data access to Repo
- Operates on Types only, receives Repo via dependency injection
- Pure business logic that is testable with mocked repos

### Runtime (Layer 4) — `src/runtime/`
- Server bootstrap (FastAPI app creation, middleware registration)
- Dependency injection wiring
- Lifecycle hooks (startup, shutdown)
- Health checks, readiness probes

### UI (Layer 5) — `src/ui/`
- FastAPI route handlers, CLI commands
- Request/response formatting
- Input validation at the boundary
- Route guards and permission checks

## Intentional Constraints

These are deliberate design choices, not oversights:

1. **Service has no direct I/O** -- all database, HTTP, and filesystem access goes through Repo. This keeps business logic testable without infrastructure.

2. **Types has no project imports** -- it depends only on stdlib and pydantic. This keeps it the stable foundation that all other layers build on.

3. **No global mutable state** -- configuration is loaded once in Config and injected forward. No module-level singletons.

4. **No cross-layer type definitions** -- a type used by multiple layers must live in Types, not defined inline in the layer that first needs it.

5. **No raw primitives for domain concepts** -- use refined Pydantic types (`UserId`, `Email`, `Amount`) instead of bare `str`, `int`, `float`. This makes code self-documenting and enforces validation at parse boundaries.

## Cross-Cutting Concerns

### Logging
Every module uses structured logging:
```python
import logging
logger = logging.getLogger(__name__)
```
Never use `print()` or `console.log()`.

### Error Handling
- External calls (API, DB, filesystem) wrapped in try/except **in the Repo layer**
- Catch specific exceptions, not bare `except:`
- Custom exception classes defined in Types, raised by Service, caught by UI
- Log context with every error

### Authentication
- Auth types (tokens, claims, roles) defined in **Types**
- Auth validation logic in **Service**
- Auth middleware registered in **Runtime**
- Route guards applied in **UI**

## Enforcement

The `.claude/linters/layer_deps.py` linter automatically checks all imports in `src/` against these rules. It runs:
- Automatically after every file write to `src/`
- As part of `python3 .claude/linters/lint_all.py`
- In CI on every push

When a violation is detected, the linter reports the exact file, line, and forbidden import direction. Fix by moving the import target to a lower layer or restructuring the dependency.
