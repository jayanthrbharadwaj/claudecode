---
disable-model-invocation: true
---

# /forge:skills

List all available forge skills with their descriptions and invocation types.

## When to Use

- You want to see what skills are available
- You need to understand the difference between auto-invoked and manual skills
- You want to find the right skill for a specific task

## Arguments

None.

## Process

1. Scan `.claude/skills/` for all `SKILL.md` files
2. Read the YAML frontmatter from each skill to extract:
   - `description`: What the skill does
   - `disable-model-invocation`: Whether it's manual-only (true) or auto-invoked (absent/false)
3. Display a formatted table:

| Skill | Type | Description |
|-------|------|-------------|
| routing | Auto | Request classifier and router |
| sdlc-pipeline | Manual | Full 11-phase pipeline |
| ... | ... | ... |

4. Group by type: auto-invoked skills first, then manual skills
