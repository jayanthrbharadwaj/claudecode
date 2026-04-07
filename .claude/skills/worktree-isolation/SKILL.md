---
description: "Git worktree isolation for story-level implementation"
disable-model-invocation: true
---

# Worktree Isolation

Isolates story implementation in git worktrees so that each story is developed independently without affecting the main working tree.

## Process

### 1. Find Next Story

Read `specs/stories/*.md` to find the next unimplemented story:

1. Read `specs/pipeline_status.md` to determine the active feature
2. Read the stories file for that feature
3. Identify stories not yet marked as complete
4. Respect the dependency graph: only pick stories whose dependencies are all complete

### 2. Create Worktree

Use Claude Code's built-in `EnterWorktree` tool to create an isolated worktree:

```
EnterWorktree: name = "story-<US-XXX>"
```

This creates a new branch and switches the session's working directory to the worktree. The main working tree is unaffected.

### 3. Implement in Isolation

Within the worktree:

1. Invoke the **implementer** agent (via Task tool) for the selected story:
   > You are an implementer agent. Implement story US-XXX following the layer architecture. The spec is at `specs/features/<feature>.md`, the story is at `specs/stories/<feature>.md`, and the design is at `specs/design/<feature>.md`. Implement layer by layer: Types -> Config -> Repo -> Service -> Runtime -> UI.

2. The implementer works entirely within the worktree branch

### 4. Validate

Run quality checks within the worktree:

```bash
python3 .claude/linters/lint_all.py
pytest tests/ --cov=src --cov-fail-under=80
```

If linters or tests fail, fix issues before committing.

### 5. Commit

Commit all changes with a conventional commit message:

```
feat(US-XXX): <story title>
```

For example: `feat(US-001): add user registration endpoint`

### 6. Worktree Cleanup

On session exit, Claude Code automatically prompts the user to keep or remove the worktree. If the user keeps it:
- The branch remains available for merging
- The user can merge it into the feature branch when ready

## Multiple Stories

To implement multiple stories in parallel using worktrees:

1. Create one worktree per story (each on its own branch)
2. Implement stories in parallel (independent stories only)
3. Merge completed story branches into the feature branch in dependency order

## When to Use

- When implementing a single story and you want to keep the main tree clean
- When experimenting with an implementation approach without risk
- When multiple stories can be worked on in parallel

## Limitations

- Cannot create a worktree if already in a worktree
- Must be in a git repository
- Story dependencies must be resolved before starting dependent stories in worktrees
