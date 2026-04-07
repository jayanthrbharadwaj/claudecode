<!-- AGENT: Do not read during exploration. This template is used only when creating specs. Read .claude/docs/scaffold-overview.md instead. -->
# Feature: [Feature Name]

**ID**: [feature-id]
**Priority**: [high | medium | low]
**Status**: [draft | review | approved | implemented | verified]

## Description

Brief, clear description of what this feature does and the problem it solves.

## Motivation

Why this feature is needed. What user problem or business need does it address?

## Technology Context

> Only list what this feature specifically requires. Skip sections that don't apply.

- **Libraries/packages**: [any new dependencies this feature introduces]
- **External services**: [APIs, databases, third-party services this feature talks to]
- **Environment variables**: [new env vars needed, with example values]

## Acceptance Criteria

Testable criteria in Given/When/Then format. Each criterion becomes a test.

1. **AC-001**: Given [precondition], When [action], Then [expected outcome]
2. **AC-002**: Given [precondition], When [action], Then [expected outcome]
3. **AC-003**: Given [error condition], When [action], Then [error handling]

## Affected Layers

- [ ] **Types** (`src/types/`): [what changes — new models, enums, etc.]
- [ ] **Config** (`src/config/`): [what changes — new env vars, settings]
- [ ] **Repo** (`src/repo/`): [what changes — new queries, API clients]
- [ ] **Service** (`src/service/`): [what changes — business logic]
- [ ] **Runtime** (`src/runtime/`): [what changes — middleware, lifecycle]
- [ ] **UI** (`src/ui/`): [what changes — routes, components]

## Data Model

> Define every field, type, and constraint. The agent writes code directly from this.

```python
class Example(BaseModel):
    """Describe what this model represents."""
    id: ExampleId          # Primary key — use refined type, not raw int
    name: str              # Human-readable name, max 100 chars
    status: ExampleStatus  # Enum: active, inactive, archived
    created_at: datetime   # Auto-set on creation
    metadata: dict | None = None  # Optional JSON blob
```

### Database Changes

> If this feature adds or modifies tables, list every column.

| Table | Column | Type | Constraints | Notes |
|-------|--------|------|-------------|-------|
| `examples` | `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | |
| `examples` | `name` | `TEXT` | `NOT NULL, UNIQUE` | Max 100 chars |
| `examples` | `status` | `TEXT` | `NOT NULL DEFAULT 'active'` | Enum: active/inactive/archived |
| `examples` | `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | |

## API Endpoints

> Define every endpoint this feature adds or modifies. Include request/response bodies.

### `POST /api/examples` — Create an example

**Request:**
```json
{
  "name": "My Example",
  "metadata": {"key": "value"}
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "My Example",
  "status": "active",
  "created_at": "2026-01-15T10:30:00Z",
  "metadata": {"key": "value"}
}
```

**Errors:**

| Status | Condition | Response body |
|--------|-----------|---------------|
| `400` | Name is empty or exceeds 100 chars | `{"error": "validation_error", "message": "Name must be 1-100 characters"}` |
| `409` | Name already exists | `{"error": "conflict", "message": "An example with this name already exists"}` |

### `GET /api/examples` — List examples

**Query params:** `?status=active&limit=20&offset=0`

**Response (200):**
```json
{
  "items": [{"id": 1, "name": "My Example", "status": "active", "created_at": "..."}],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

## UI Changes

> Skip this section if the feature has no user-facing changes.

### Layout

Describe where new UI elements appear and how they relate to existing layout:
- [e.g., "Add a 'Create Example' button in the top-right of the examples list page"]
- [e.g., "New modal dialog for example creation, triggered by the button"]

### Components

| Component | Location | Behavior |
|-----------|----------|----------|
| `CreateExampleButton` | `src/ui/examples/` | Opens creation modal on click |
| `ExampleForm` | `src/ui/examples/` | Validates name length, shows inline errors |
| `ExampleList` | `src/ui/examples/` | Paginated list with status filter dropdown |

### Visual Specs

> Include if relevant: colors, spacing, typography, responsive behavior.

- Button style: primary action (matches existing design system)
- Error text: red (#DC2626), 14px, below the input field
- List items: 48px height, hover highlight, truncate name at 40 chars

## User Interaction Flow

> Step-by-step walkthrough of how a user interacts with this feature.

1. User navigates to the examples page
2. User clicks "Create Example" button
3. Modal opens with name input and optional metadata fields
4. User enters name and clicks "Save"
5. If validation fails → inline error message appears, modal stays open
6. If save succeeds → modal closes, new example appears at top of list
7. Toast notification confirms "Example created"

## Business Rules

> Precise, testable statements. Each rule should map to one or more acceptance criteria.

1. Example names must be unique (case-insensitive)
2. Example names must be 1-100 characters, alphanumeric plus spaces and hyphens
3. Newly created examples always start with status "active"
4. Deleting an example soft-deletes it (sets status to "archived"), not hard-delete

## Edge Cases

> What happens at boundaries? Agents need these to write correct code.

1. **Empty name** → validation error, example not created
2. **Name with 100 chars** → accepted (boundary)
3. **Name with 101 chars** → validation error
4. **Duplicate name (different case)** → conflict error ("My Example" vs "my example")
5. **Create while offline** → error toast, form state preserved for retry

## Error Handling

| Error Condition | Layer | Error Type | User-Facing Message |
|----------------|-------|-----------|---------------------|
| Name too long | Service | `ValidationError` | "Name must be 1-100 characters" |
| Duplicate name | Repo | `ConflictError` | "An example with this name already exists" |
| Database unreachable | Repo | `ConnectionError` | "Unable to save. Please try again." |

## Implementation Order

> The agent implements in this order. Each step should be independently testable.

1. **Types**: Add `ExampleId`, `ExampleStatus` enum, `Example` model
2. **Repo**: Add `ExampleRepo` with `create()`, `list()`, `get_by_id()` methods
3. **Service**: Add `ExampleService` with business rule validation
4. **Runtime**: Register `ExampleService` in dependency injection
5. **UI**: Add route handler, form component, list component

## Dependencies

- **Features**: [other feature specs this depends on — e.g., "user-auth.md"]
- **External**: [third-party services, APIs, libraries]

## Test Strategy

> Map tests to acceptance criteria. The agent writes these alongside implementation.

- **Unit tests**: Test `ExampleService` validation rules (mock repo). Covers AC-001, AC-003.
- **Integration tests**: Test `ExampleRepo` with in-memory SQLite. Covers AC-002.
- **E2E tests**: Test full create flow through UI. Covers AC-001 end-to-end.

## Success Criteria

> How do we know this feature is done? Measurable, verifiable checks.

- [ ] All acceptance criteria have passing tests
- [ ] Coverage for new code is >= 80%
- [ ] All linters pass (`python3 .claude/linters/lint_all.py`)
- [ ] API responses match the documented schemas exactly
- [ ] UI matches the visual specs described above
- [ ] No console errors or unhandled exceptions
- [ ] Edge cases are handled gracefully with user-friendly messages

## Non-Functional Requirements

- **Performance**: [e.g., "List endpoint responds in < 200ms for 1000 examples"]
- **Security**: [e.g., "Only authenticated users can create examples"]
- **Scalability**: [e.g., "Pagination required — never load all examples at once"]

## Open Questions

> These MUST be resolved before status moves to "approved". Agents stop and ask if they encounter these.

- [ ] [Any unresolved decisions or clarifications needed]

## Estimated Complexity

**[Small | Medium | Large]** — [justification]
