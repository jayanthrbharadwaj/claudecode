---
description: "Single task execution with TDD enforcement and post-task validation"
disable-model-invocation: true
---

# Execute Task

Executes a single task (story or work item) with strict TDD and post-task validation.

## Process

1. **Identify the task** — read from story ID, task ID, or user description
2. **Read context**:
   - Feature spec: `specs/features/<feature>.md`
   - Design doc: `specs/design/<feature>.md`
   - Existing code in target layers
3. **Invoke task-executor agent** via Task tool:
   ```
   Task:
     subagent_type: "general-purpose"
     prompt: "You are the task-executor agent. Read .claude/agents/task-executor.md. Implement story <US-XXX> using strict TDD for each acceptance criterion."
   ```
4. **Verify results**:
   - All tests pass: `pytest tests/ -x -q`
   - Linters pass: `python3 .claude/linters/lint_all.py`
   - Commit exists: `feat(US-XXX): <description>`
5. **Run task-validation-loop** — invoke the task-validation-loop skill
6. **Handle validation failures** — if checkers fail, re-invoke task-executor with findings (max 3 cycles)

## Rules

- TDD is mandatory — every acceptance criterion gets RED-GREEN-REFACTOR
- Post-task validation always runs after implementation
- One commit per story
- Max 3 validation retry cycles
