<!-- AGENT: Do not read during exploration. This template is used only when creating specs. Read .claude/docs/scaffold-overview.md instead. -->
# User Stories: [Feature Name]

**Feature Spec**: `specs/features/[feature-name].md`
**Created**: [YYYY-MM-DD]

## Story Map

| ID | Story | Depends On | Layer(s) | Complexity |
|----|-------|-----------|----------|------------|
| US-001 | As a [role], I want [action], so that [benefit] | — | Service, Repo | Small |
| US-002 | As a [role], I want [action], so that [benefit] | US-001 | Service, UI | Medium |
| US-003 | As a [role], I want [action], so that [benefit] | — | Types, Config | Small |

## Dependency Graph

```
US-003 (Types/Config)
  └── US-001 (Service/Repo)
        └── US-002 (Service/UI)

US-004 ──── (independent)
```

## Parallel Groups

Stories with no dependency relationship can be implemented simultaneously.

| Group | Stories | Rationale |
|-------|---------|-----------|
| A | US-003, US-004 | No shared layers or data dependencies |
| B | US-001 | Depends on Group A |
| C | US-002 | Depends on US-001 |

## Story Details

### US-001: [Short title]

**As a** [role], **I want** [action], **so that** [benefit].

**Acceptance Criteria**:
1. Given [precondition], When [action], Then [outcome]
2. Given [precondition], When [action], Then [outcome]

**Notes**: [Implementation hints, constraints, or edge cases]

### US-002: [Short title]

**As a** [role], **I want** [action], **so that** [benefit].

**Acceptance Criteria**:
1. Given [precondition], When [action], Then [outcome]
2. Given [precondition], When [action], Then [outcome]

**Notes**: [Implementation hints, constraints, or edge cases]
