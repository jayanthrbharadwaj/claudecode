---
disable-model-invocation: true
---

# /forge:work-on

Work on a specific task or story with TDD enforcement.

## When to Use

- You want to implement a specific story (not just the next one)
- You have a task ID from `/forge:create-tasks` and want to work on it
- You want TDD-enforced implementation for a single unit of work

## Arguments

- **target** (required): Story ID (e.g., `US-001`) or task ID

## Process

1. Invoke the `execute-task` skill with the specified target
2. Read the story/task details and acceptance criteria
3. For each acceptance criterion, follow strict TDD:
   a. Write a failing test (RED)
   b. Write minimum code to pass (GREEN)
   c. Refactor (REFACTOR)
4. Run linters and full test suite
5. Commit with `feat(US-XXX): <description>`
6. Run post-task validation (architecture-alignment, design-consistency, prd-architecture)
7. Report results
