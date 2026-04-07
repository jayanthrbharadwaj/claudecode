---
disable-model-invocation: true
---

# /forge:work-on-next

Pick the next unimplemented user story and work on it in an isolated git worktree.

## When to Use

Use this command for incremental, story-by-story implementation. This is ideal when:
- You want to implement and review one story at a time
- You prefer isolated branches per story for cleaner git history
- You want to pause between stories for review

## Arguments

- **story-id** (optional): A specific story ID to work on (e.g., `US-003`). If omitted, the next unimplemented story is picked automatically.

Examples:
- `/forge:work-on-next` — picks the next unimplemented story
- `/forge:work-on-next US-005` — works on a specific story

## Process

### 1. Identify the Target Story
1. If a story ID was provided, read `specs/stories/<story-id>.md`.
2. If no story ID was provided, scan `specs/stories/` for all story files.
3. Read `specs/pipeline_status.md` (or each story file's status) to find the first story marked as **not implemented**.
4. If all stories are implemented, inform the user and suggest `/forge:validate` or `/forge:review`.

### 2. Create Isolated Worktree
5. Use the **EnterWorktree** tool to create a worktree named `story-<US-XXX>` (e.g., `story-US-003`).
6. This automatically creates a new branch and switches the session to the worktree directory.

### 3. Implement the Story
7. Read the story file (`specs/stories/<US-XXX>.md`) for acceptance criteria and requirements.
8. Read the execution plan (`specs/plans/`) for implementation guidance and layer ordering.
9. Read the design document (`specs/design/`) for architectural context.
10. Invoke the **implementer** agent to implement the story layer-by-layer following the 6-layer architecture.

### 4. Verify Quality
11. Run `python3 .claude/linters/lint_all.py` to check linter compliance.
12. Run `make test` to verify all tests pass.
13. If linters or tests fail, fix issues and re-run until passing.

### 5. Commit
14. Stage all changes related to the story.
15. Commit with message format: `feat(US-XXX): <story description>`
16. Example: `feat(US-003): add user registration with email verification`

### 6. Report and Prompt
17. Report what was implemented, tests passing, and linter status.
18. Inform the user that the worktree is active and they will be prompted to keep or merge it on session exit.
19. Suggest next steps:
    - `/forge:work-on-next` for the next story
    - `/forge:review` to run reviews on the current work
    - `/forge:create-pr` to create a PR for this story
