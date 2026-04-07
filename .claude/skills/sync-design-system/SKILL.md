---
description: "Discover UI patterns from code and generate design system documentation"
disable-model-invocation: true
---

# Sync Design System

Reverse-engineers a design system document by analyzing existing UI code.

## Process

1. **Scan UI code**:
   a. Find all files in `src/ui/`, `templates/`, and static asset directories
   b. Extract color values (hex, rgb, CSS variables)
   c. Extract spacing values (margins, padding, gaps)
   d. Extract typography (font families, sizes, weights)
   e. Identify component patterns (repeated HTML/template structures)

2. **Identify patterns**:
   a. Group similar color values into a palette
   b. Identify a spacing scale from recurring values
   c. Map typography to heading/body/caption roles
   d. Catalog recurring component patterns (buttons, cards, forms)

3. **Generate design system document**:
   - Color palette with named tokens
   - Spacing scale
   - Typography scale
   - Component catalog with usage examples
   - Interaction patterns (loading, error, empty states)

4. **Write to `specs/design_system.md`** or present for review

## Rules

- Only document patterns that exist in code — do not invent a design system
- Group similar values (e.g., #333 and #334 are likely the same intended color)
- If no UI code exists, report that and skip
- Flag inconsistencies (e.g., 5 different grays) as improvement opportunities
