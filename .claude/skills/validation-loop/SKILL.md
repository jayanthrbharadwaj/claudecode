---
description: "8 parallel reviewer agents with unanimous approval requirement and max 3 retry cycles"
disable-model-invocation: true
---

# Validation Loop

Replaces the sequential 3-reviewer pattern with 8 parallel reviewers. All gating reviewers must approve unanimously. Max 3 retry cycles.

## Reviewers (8)

### Gating Reviewers (block PR)

| # | Agent | Question |
|---|-------|----------|
| 1 | spec-reviewer | Does the implementation match the spec? |
| 2 | code-reviewer | Is code quality acceptable? |
| 3 | security-reviewer | Is the code secure? |
| 4 | performance-reviewer | Are there performance issues? |
| 5 | architecture-alignment-checker | Does code align with architecture docs? |

### Advisory Reviewers (inform but don't block)

| # | Agent | Question |
|---|-------|----------|
| 6 | design-consistency-checker | Does UI comply with design system? |
| 7 | code-simplifier | Is there over-engineering? |
| 8 | prd-architecture-checker | Do architecture docs match requirements? |

## Process

### Round 1: Parallel Review

Invoke all 8 reviewers in parallel via the Task tool:

```
For each reviewer:
  Task:
    subagent_type: "general-purpose"
    prompt: "You are the <agent-name> agent. Read .claude/agents/<agent-name>.md. Review the implementation in src/ against specs/features/<feature>.md. Produce your review report."
```

Wait for all 8 to complete.

### Round 2: Collect Verdicts

Parse each reviewer's output:
- **Gating reviewers** (1-5): APPROVE or REQUEST_CHANGES
- **Advisory reviewers** (6-8): Always ADVISORY — include in report but never block

### Round 3: Fix-and-Retry (if needed)

If any gating reviewer returns REQUEST_CHANGES:
1. Collect all findings from failing reviewers
2. Re-invoke the implementer with the combined findings list
3. After fixes, re-invoke ONLY the failing reviewers (not all 8)
4. Repeat until all gating reviewers approve or max 3 cycles reached

### Round 4: Escalate (if still failing)

If any gating reviewer still fails after 3 cycles:
1. Present all remaining findings to the user
2. Ask the user how to proceed (fix manually, override, or abandon)

## Output

Combined validation report saved to `specs/review_report.md`:

```markdown
# Validation Report
Generated: <timestamp>
Cycle: <cycle-number>/3

## Gating Reviews
| Reviewer | Verdict | Cycle | Notes |
|----------|---------|-------|-------|
| spec-reviewer | APPROVE | 1 | All criteria matched |
| code-reviewer | APPROVE | 2 | Fixed naming in cycle 1 |
| security-reviewer | APPROVE | 1 | No issues |
| performance-reviewer | APPROVE | 1 | No N+1 queries |
| architecture-alignment | APPROVE | 1 | All layers correct |

## Advisory Reviews
| Reviewer | Findings | Notes |
|----------|----------|-------|
| design-consistency | 2 suggestions | Minor spacing inconsistencies |
| code-simplifier | 1 suggestion | Factory pattern could be simplified |
| prd-architecture | ALIGNED | All requirements covered |
```

## Rules

- ALL 5 gating reviewers must approve — unanimous approval required
- Advisory reviewers NEVER block — their findings are informational
- Run gating reviewers in parallel for speed
- On retry, only re-run failing reviewers (not all 8)
- Max 3 retry cycles before escalating to human
- Always include advisory findings in the report even if gating passes
