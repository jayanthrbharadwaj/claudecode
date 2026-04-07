---
description: "Parse natural-language feature requests into structured feature briefs"
disable-model-invocation: true
---

# Understanding Feature Requests

Parses a natural-language feature description into a structured brief suitable for implementation.

## Process

1. **Receive** the user's natural-language description
2. **Extract** the following from the description:
   - **Feature name**: Short identifier (kebab-case)
   - **Summary**: One-sentence description of what the feature does
   - **Core requirements**: Numbered list of what the feature must do
   - **Acceptance criteria**: Given/When/Then format for each requirement
   - **Affected layers**: Which layers of the 6-layer architecture are impacted
   - **Data model changes**: New or modified Pydantic types needed
   - **API changes**: New or modified endpoints
   - **Constraints**: Things to avoid or limitations to respect
3. **Validate** the brief:
   - Every requirement has at least one acceptance criterion
   - Affected layers are valid (Types, Config, Repo, Service, Runtime, UI)
   - No acceptance criterion is ambiguous or untestable
4. **Return** the structured brief

## Output Format

```markdown
## Feature Brief: <feature-name>

**Summary**: <one-sentence description>

### Requirements
1. <requirement>
2. <requirement>

### Acceptance Criteria
- AC-1: Given <precondition>, When <action>, Then <outcome>
- AC-2: Given <precondition>, When <action>, Then <outcome>

### Affected Layers
- Types: <new types needed>
- Repo: <new data access needed>
- Service: <new business logic>
- UI: <new endpoints/handlers>

### Constraints
- <constraint>
```

## Rules

- If the description is too vague, ask clarifying questions before producing the brief
- Every requirement must be testable — no vague language like "should be fast" or "user-friendly"
- Keep the brief concise — this is not a full spec
