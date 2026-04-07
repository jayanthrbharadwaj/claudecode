<!-- AGENT: Do not read during exploration. This template is used only when creating specs. Read .claude/docs/scaffold-overview.md instead. -->
# Feature: [Feature Name]

**ID**: [feature-id]
**Priority**: [high | medium | low]
**Status**: [draft | review | approved | implemented | verified]

## Description

Brief, clear description of what this feature does and the problem it solves.

## Acceptance Criteria

1. **AC-001**: Given [precondition], When [action], Then [expected outcome]
2. **AC-002**: Given [precondition], When [action], Then [expected outcome]
3. **AC-003**: Given [error condition], When [action], Then [error handling]

## Affected Layers

- [ ] **Types** (`src/types/`): [what changes]
- [ ] **Config** (`src/config/`): [what changes]
- [ ] **Repo** (`src/repo/`): [what changes]
- [ ] **Service** (`src/service/`): [what changes]
- [ ] **Runtime** (`src/runtime/`): [what changes]
- [ ] **UI** (`src/ui/`): [what changes]

## Business Rules

1. [Precise, testable statement]
2. [Precise, testable statement]

## Edge Cases

1. [Boundary condition] → [expected behavior]
2. [Error condition] → [expected behavior]

## Error Handling

| Error Condition | Layer | User-Facing Message |
|----------------|-------|---------------------|
| [condition] | [layer] | [message] |

## Implementation Order

1. **Types**: [what to add]
2. **Repo**: [what to add]
3. **Service**: [what to add]
4. **Runtime**: [what to wire up]
5. **UI**: [what to add]

## Test Strategy

- **Unit tests**: [what to test, which ACs covered]
- **Integration tests**: [what to test]

## Open Questions

- [ ] [Any unresolved decisions]
