---
description: "Team orchestration lifecycle using Claude Code agent teams: create teams, assign tasks, spawn teammates, monitor, enforce quality gates, cleanup"
disable-model-invocation: true
---

# Teams

Activates Claude Code agent teams for parallel implementation. Each teammate is a fully independent Claude Code session with its own context window. Teammates coordinate through a shared task list and direct messaging.

> Agent teams are experimental. Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json env (already configured).

## When to Use

This skill is invoked by Phase 6 of the SDLC pipeline when the mechanical team threshold is met (4+ stories AND 2+ parallel groups). It can also be invoked directly via `/forge:create-tasks` for manual team setup.

## Prerequisites

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` must be `1` in `.claude/settings.json` env
- Stories file must exist: `specs/stories/<feature-name>.md`
- Stories must have a dependency graph with parallel groups

## Team Lifecycle

### 1. Create Team

The lead (main conversation) creates the team:

```
TeamCreate:
  team_name: "feat-<feature-name>"
  description: "Implementing <feature-name> with <N> stories in <M> parallel groups"
```

This creates:
- Team config at `~/.claude/teams/feat-<feature-name>/config.json`
- Shared task list at `~/.claude/tasks/feat-<feature-name>/`

### 2. Create Tasks from Stories

Read `specs/stories/<feature-name>.md` and create one task per story:

```
For each story US-XXX:
  TaskCreate:
    subject: "US-XXX: <story title>"
    description: |
      Story: <full story text with acceptance criteria>
      Spec: specs/features/<feature-name>.md
      Design: specs/design/<feature-name>.md
      Layer impact: <layers affected>
      Files to own: <list of files this story touches>
    activeForm: "Implementing US-XXX: <title>"

  If story depends on US-YYY:
    TaskUpdate:
      taskId: <task-id-for-US-XXX>
      addBlockedBy: [<task-id-for-US-YYY>]
```

Task dependencies auto-unblock: when a teammate completes a task, any tasks blocked by it automatically become available.

### 3. Spawn Teammates

One teammate per parallel group. Each teammate is a full, independent Claude Code session spawned via the Task tool:

```
Task:
  subagent_type: "general-purpose"
  team_name: "feat-<feature-name>"
  name: "implementer-group-<N>"
  mode: "bypassPermissions"
  prompt: |
    You are an implementer teammate on team feat-<feature-name>.
    Read your instructions from .claude/agents/implementer.md.
    Read .claude/agents/task-executor.md for TDD enforcement.

    IMPORTANT: You are a full Claude Code session with your own context window.
    You share a task list with other teammates. Coordinate through tasks and messages.

    Your workflow:
    1. Call TaskList to see available tasks
    2. Claim an unblocked, unassigned task with TaskUpdate (set owner to your name)
    3. Read the task details with TaskGet — it contains the story and acceptance criteria
    4. Implement the story using strict TDD (RED-GREEN-REFACTOR for each AC)
    5. IMPORTANT: Only modify files listed in your task description to avoid conflicts with other teammates
    6. Run linters: python3 .claude/linters/lint_all.py
    7. Run tests: pytest tests/ -x -q
    8. Commit: feat(US-XXX): <description>
    9. Mark task complete with TaskUpdate (status: "completed")
    10. Send completion message to the team lead via SendMessage:
        SendMessage(type="message", recipient="<lead-name>", content="Completed US-XXX. Tests passing.", summary="Completed US-XXX")
    11. Check TaskList for next unblocked, unassigned task
    12. Repeat until no tasks remain
    13. When done, send final message: SendMessage(type="message", recipient="<lead-name>", content="All my tasks complete.", summary="All tasks done")
```

**Teammate behavior notes** (from official docs):
- Each teammate loads project context (CLAUDE.md, MCP servers, skills) but NOT the lead's conversation history
- Task claiming uses file locking to prevent race conditions
- Teammates can message each other directly, not just the lead
- Idle notifications are sent automatically when a teammate finishes its turn

**Plan approval** (for complex stories):
To require a teammate to plan before implementing, add `mode: "plan"` to the Task call. The teammate works in read-only plan mode until the lead approves:

```
Task:
  subagent_type: "general-purpose"
  team_name: "feat-<feature-name>"
  name: "implementer-group-<N>"
  mode: "plan"
  prompt: "Plan the implementation for Group <N> stories before making any changes."
```

### 4. Monitor Progress

The lead monitors via multiple channels:

- **TaskList** — poll task statuses (pending, in_progress, completed)
- **Automatic messages** — teammates send SendMessage on task completion
- **Idle notifications** — system notifies lead when a teammate finishes its turn
- **Direct interaction** — use Shift+Down (in-process mode) to cycle through teammates and message them directly

**If a teammate gets stuck**: message it directly with guidance or reassign its task to another teammate.

**If the lead starts implementing instead of waiting**: tell it "Wait for your teammates to complete their tasks before proceeding."

### 5. Post-Implementation Verification

After all tasks are complete:

1. Run full test suite: `pytest tests/ --cov=src --cov-fail-under=80`
2. Run all linters: `python3 .claude/linters/lint_all.py`
3. Verify all acceptance criteria are covered
4. Check for file conflicts between teammates (if any, resolve before continuing)

### 6. Graceful Shutdown and Cleanup

Always follow this order — cleanup fails if teammates are still active:

1. **Shutdown each teammate**:
   ```
   For each teammate:
     SendMessage:
       type: "shutdown_request"
       recipient: "<teammate-name>"
       content: "All tasks complete. Please shut down."
   ```
   Each teammate receives the request and responds with `shutdown_response` (approve to exit, reject to continue).

2. **Wait for all shutdown confirmations**

3. **Clean up team resources**:
   ```
   TeamDelete
   ```
   This removes `~/.claude/teams/feat-<feature-name>/` and `~/.claude/tasks/feat-<feature-name>/`.

**IMPORTANT**: Only the lead should run TeamDelete. Teammates must not run cleanup — their team context may not resolve correctly.

## Display Modes

Agent teams support two display modes (configured in settings.json via `teammateMode`):

| Mode | Description | Requirements |
|------|-------------|-------------|
| `in-process` | All teammates run in main terminal. Shift+Down to cycle. | Any terminal |
| `tmux` | Each teammate gets its own pane. Click to interact. | tmux or iTerm2 |
| `auto` (default) | Uses tmux if in tmux session, otherwise in-process | Varies |

## Quality Gate Hooks

Two hook events enforce quality when teammates finish work:

### TeammateIdle Hook
Runs when a teammate is about to go idle. Exit code 2 sends feedback and keeps the teammate working:
- Checks if the teammate's assigned tasks are truly complete
- Verifies tests pass for the teammate's changes
- If checks fail, exits with code 2 to keep the teammate working

### TaskCompleted Hook
Runs when a task is being marked complete. Exit code 2 prevents completion and sends feedback:
- Verifies the task's acceptance criteria are covered by tests
- Runs linters on changed files
- If checks fail, exits with code 2 to reject completion

## Avoiding File Conflicts

Two teammates editing the same file causes overwrites. Prevent this by:
- Assigning file ownership in task descriptions ("Files to own: src/repo/users.py, tests/test_users.py")
- Breaking stories so each touches different files
- If conflict is unavoidable, make one story depend on the other (sequential, not parallel)

## Error Handling

| Error | Recovery |
|-------|----------|
| Teammate fails a task | Lead re-assigns to another teammate or handles directly |
| Teammate stops on error | Message it directly with Shift+Down, or spawn a replacement |
| Team creation fails | Fall back to sequential implementation with single task-executor |
| Task status lags | Check if work is done, update status manually via TaskUpdate |
| Teammate doesn't shut down | Wait for current request to finish, then retry shutdown |

Max 3 retry cycles per failed task before escalating to the user.

## Task Sizing

From the official best practices:
- **Too small**: coordination overhead exceeds benefit
- **Too large**: teammates work too long without check-ins
- **Just right**: self-contained units producing a clear deliverable (one story = one task)
- Aim for 5-6 tasks per teammate to keep everyone productive

## Architecture Reference

```
Team config:  ~/.claude/teams/{team-name}/config.json
Task list:    ~/.claude/tasks/{team-name}/
Team lead:    Main conversation (creates team, coordinates)
Teammates:    Independent Claude Code sessions (own context window each)
Messaging:    SendMessage (direct) or broadcast (all teammates)
```

The team config `members` array contains each teammate's `name`, `agentId`, and `agentType`. Teammates can read this to discover other team members.

## Known Limitations

These are upstream constraints of the agent teams feature:

- **No session resumption for teammates**: `/resume` and `/rewind` do not restore in-process teammates. After resuming, the lead should spawn new teammates.
- **Task status can lag**: Teammates sometimes fail to mark tasks complete, blocking dependents. Check manually and update via TaskUpdate.
- **Shutdown can be slow**: Teammates finish their current request or tool call before shutting down.
- **Lead is fixed**: The session that creates the team is the lead for its lifetime. You cannot promote a teammate to lead.
- **Permissions set at spawn**: All teammates start with the lead's permission mode. You can change individual modes after spawning but not at spawn time.
- **Split panes unsupported in some terminals**: Split-pane mode is not supported in VS Code's integrated terminal, Windows Terminal, or Ghostty.

## Token Usage

Agent teams use significantly more tokens than a single session. Each teammate has its own context window, and token usage scales linearly with the number of active teammates. Start with 3-5 teammates for most workflows (one per parallel group). For routine tasks, a single session is more cost-effective.

## Rules

- MUST use teams when 4+ stories AND 2+ parallel groups (mechanical check)
- One task per story — never combine stories into a single task
- Tasks must have correct dependency blocking from the story dependency graph
- Each teammate should own a distinct set of files — no overlapping edits
- Always run full test suite after all tasks complete
- Always shut down all teammates before running TeamDelete
- Only the lead runs TeamDelete — never a teammate
- One team per session — clean up current team before starting a new one
- No nested teams — teammates cannot spawn their own teams
