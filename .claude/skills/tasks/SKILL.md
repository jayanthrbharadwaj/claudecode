---
description: "Task management: create tasks from stories, list, update, and track progress"
disable-model-invocation: true
---

# Tasks

Manages the task lifecycle: creation from stories, status tracking, and progress reporting.

## Actions

### create

Create tasks from user stories:

1. Read stories from `specs/stories/<feature>.md`
2. Parse the dependency graph and parallel groups
3. For each story, call TaskCreate:
   - subject: `US-XXX: <title>`
   - description: Full story text with acceptance criteria, layer impact
   - activeForm: `Implementing US-XXX: <title>`
4. Set up dependency blocking via TaskUpdate with `addBlockedBy`
5. Display the created task list

### list

Display current tasks with status:

1. Call TaskList
2. Format as table: ID | Story | Status | Owner | Blocked By
3. Show progress: X of Y completed

### update

Update a task's status:

1. Call TaskUpdate with the specified task ID and new status
2. Display confirmation

### progress

Show implementation progress:

1. Call TaskList
2. Calculate: total, pending, in_progress, completed, blocked
3. Display progress bar and summary
4. List any blocked tasks and their blockers

## Rules

- One task per story — never merge stories into a single task
- Dependencies must match the story dependency graph exactly
- Task descriptions must include acceptance criteria for the implementer
