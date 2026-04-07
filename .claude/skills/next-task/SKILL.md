---
description: "Pick the next unblocked, unassigned task from the backlog and execute it"
disable-model-invocation: true
---

# Next Task

Finds and executes the next available task from the project backlog.

## Process

1. **Find the next task**:
   a. Read `specs/plans/<feature>.md` execution plan for story ordering
   b. If using TaskList (team context): find tasks with status `pending`, no owner, and empty `blockedBy`
   c. If no task system: find the next uncompleted story from the stories file
2. **Select the task** — prefer the lowest-numbered unblocked task (earlier stories set context for later ones)
3. **Execute** — invoke the `execute-task` skill with the selected task
4. **Report** — display what was completed and what's next in the backlog

## Rules

- Always check for blocking dependencies before starting a task
- Prefer story order (lowest ID first) when multiple tasks are available
- If no tasks are available, report that all tasks are complete or blocked
