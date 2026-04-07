---
description: "Structured 5-phase debugging workflow wrapping the debug-agent"
disable-model-invocation: true
---

# Debugging

Wraps the debug-agent with a structured 5-phase debugging process.

## Phases

### Phase 1: Reproduce

1. Read the bug report or user description
2. Identify the expected behavior vs actual behavior
3. Find or write a test that reproduces the issue
4. Confirm the test fails consistently

### Phase 2: Isolate

1. Narrow down the failure to a specific module/function
2. Check recent changes (git log, git diff) for likely culprits
3. Add targeted logging or debugging output
4. Identify the root cause — not just the symptom

### Phase 3: Fix

1. Write the minimum fix for the root cause
2. Do NOT fix unrelated issues or refactor surrounding code
3. Ensure the fix follows project conventions

### Phase 4: Verify

1. Run the reproduction test — must now pass
2. Run the full test suite — no regressions
3. Run linters — no new violations
4. If the bug was in a reviewed area, consider if the fix needs re-review

### Phase 5: Document

1. Add a regression test if one doesn't exist from Phase 1
2. Comment the fix if the root cause was non-obvious
3. Update any relevant specs if the bug revealed a spec gap

## Invocation

Invoke the debug-agent via Task tool:

```
Task:
  subagent_type: "general-purpose"
  prompt: "You are the debug-agent. Read .claude/agents/debug-agent.md. Debug the following issue: <issue description>. Follow the 5-phase debugging process."
```

## Rules

- Always reproduce before fixing — never guess at the fix
- Always verify the fix with tests — never assume it works
- Minimum fix only — do not scope-creep during debugging
