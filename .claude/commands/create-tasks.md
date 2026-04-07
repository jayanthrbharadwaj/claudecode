---
disable-model-invocation: true
---

# /forge:create-tasks

Create tasks from user stories using the task management system.

## When to Use

- After stories are written and you want to create trackable tasks
- When setting up team orchestration for parallel implementation
- When you want to track implementation progress story-by-story

## Arguments

- **feature** (required): Feature name (matches `specs/stories/<feature>.md`)

## Process

1. Invoke the `tasks` skill with action `create`
2. Read stories from `specs/stories/<feature>.md`
3. For each story, create a task via TaskCreate:
   - Subject: story ID and title
   - Description: acceptance criteria, layer impact, dependencies
   - Set `addBlockedBy` from the story dependency graph
4. Display the created task list with dependency relationships
5. Tasks are ready for assignment to implementer agents
