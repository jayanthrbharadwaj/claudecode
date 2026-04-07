---
description: "Feature implementation orchestrator: team threshold check, TDD enforcement, validation loops"
disable-model-invocation: true
---

# Implement Feature

Orchestrates the complete implementation of a feature from stories through validated, tested code. Handles the decision between team orchestration and sequential implementation.

## Process

### 1. Read Inputs

- Read spec: `specs/features/<feature-name>.md`
- Read stories: `specs/stories/<feature-name>.md`
- Read design: `specs/design/<feature-name>.md`
- Read execution plan: `specs/plans/<feature-name>.md`

### 2. Team Threshold Check (MANDATORY)

Count stories and parallel groups from the stories file:

| Stories | Parallel Groups | Action |
|---------|----------------|--------|
| >= 4 | >= 2 | Invoke `teams` skill for parallel implementation |
| < 4 | any | Sequential implementation with single task-executor |
| any | < 2 | Sequential implementation with single task-executor |

This is a mechanical check. Do NOT override based on judgment.

### 3a. Team Implementation (when threshold met)

1. Invoke the `teams` skill with the feature name
2. The teams skill handles: create team → create tasks → spawn agents → monitor → verify → cleanup
3. Each implementer agent uses TDD enforcement (test-driven-development skill)
4. Each implementer runs task-validation-loop after each story

### 3b. Sequential Implementation (below threshold)

For each story in dependency order:
1. Invoke the `execute-task` skill with the story
2. The execute-task skill handles: TDD cycle → linters → tests → commit → task-validation-loop
3. Move to the next story only after current story passes validation

### 4. Post-Implementation

1. Run full test suite: `pytest tests/ --cov=src --cov-fail-under=80`
2. Run all linters: `python3 .claude/linters/lint_all.py`
3. Update execution plan with progress checkboxes

## Rules

- Always check team threshold before implementation — never skip
- TDD is mandatory for every acceptance criterion
- Task-validation-loop runs after every story
- Full test suite runs after all stories are complete
