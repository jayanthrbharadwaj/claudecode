---
description: "UI/UX design system management: create, update, and enforce design tokens and patterns"
disable-model-invocation: true
---

# Design System

Manages the project's UI/UX design system documentation and enforcement.

## Actions

### create

Generate a design system document from existing UI code:

1. Scan `src/ui/` and template directories for UI patterns
2. Extract recurring patterns: components, spacing, colors, typography
3. Generate `specs/design_system.md` with:
   - Design tokens (colors, spacing, typography, breakpoints)
   - Component library (buttons, forms, cards, navigation)
   - Layout patterns (grids, containers, responsive rules)
   - Interaction patterns (loading, error, empty states)

### update

Update design system docs from code changes:

1. Read current `specs/design_system.md`
2. Scan UI code for new or changed patterns
3. Update the document to reflect current state

### enforce

Check UI code against design system:

1. Invoke the design-consistency-checker agent
2. Report findings: CONSISTENT, VIOLATION, DRIFT
3. For violations, provide the design system reference and fix suggestion

## Rules

- If no UI layer exists, skip design system operations
- Design tokens should use named values, not magic numbers
- The design system is a living document — update it as the UI evolves
