# Pipeline Orchestrator

> The main conversation drives all phases after the spec-writer completes.
> This runbook tells you exactly what to do at each phase.

## Phase Sequence

```
1. Spec → 2. Stories → 3. Design → 4. Test Plan → 5. Exec Plan
→ [APPROVE] →
6. Implement → 7. Test Fill → 8. E2E Tests → 9. DevOps
→ 10. Review → [APPROVE] → 11. PR
```

**Two human approval checkpoints**: before implementation (phase 6) and before PR (phase 11).

## Phase Gate Protocol

Before advancing to the next phase:
1. **Verify artifacts exist** — check that the expected output files were created
2. **Update `specs/pipeline_status.md`** — mark the current phase complete with timestamp

If `specs/pipeline_status.md` does not exist, copy from `.claude/templates/pipeline_status.md` and fill in the feature name.

## Cross-Turn Resumption

When a conversation starts or resumes:
1. Read `specs/pipeline_status.md`
2. Find the last completed phase
3. Resume from the next phase
4. If no pipeline_status.md exists, start fresh with routing

## Phase Details

### Phase 1: Spec

**Agent**: spec-writer
**Trigger**: User says "Build me X" or "Add feature X"
**Output**: `specs/app_spec.md` (greenfield) or `specs/features/<name>.md` (feature)
**Gate**: Spec file exists and user has reviewed it

The spec-writer handles phases 1-5 in sequence. Do not interrupt it.

### Phase 2: Stories

**Agent**: spec-writer (continues)
**Output**: `specs/stories/<name>.md`
**Gate**: Stories file exists with dependency graph and parallel groups

### Phase 3: Design

**Agent**: spec-writer (continues)
**Output**: `specs/design/<name>.md`
**Gate**: Design doc exists with layer analysis and API contracts

### Phase 4: Test Plan

**Agent**: spec-writer (continues)
**Output**: `specs/tests/<name>.md`
**Gate**: Test plan exists with test cases (TC-XXX), test types, and test data

### Phase 5: Exec Plan

**Agent**: spec-writer (continues)
**Output**: `specs/plans/<name>.md`
**Gate**: Execution plan exists with tasks, file paths, and verification steps

### APPROVAL CHECKPOINT 1

**Action**: Present the execution plan to the user and wait for explicit approval.
**Show**: Summary of stories, design decisions, test coverage, and implementation plan.
**Wait**: Do NOT proceed until the user says "approved", "go ahead", "looks good", or similar.

### Phase 6: Implement

**Agent**: implementer (or team of implementers via `teams` skill)
**Input**: Spec, stories, design, execution plan
**Output**: `src/` code + `tests/` unit/integration tests
**TDD**: Mandatory — every acceptance criterion follows RED → GREEN → REFACTOR cycle

**Team orchestration check** (MANDATORY — do not skip):
1. Read the stories file and count the total number of stories
2. Count the number of parallel groups listed in the "Parallel Groups" section
3. If story count >= 4 AND parallel group count >= 2 → you MUST invoke the `teams` skill (see Team Orchestration Protocol below). Do NOT override this based on story size, complexity, or subjective judgment.
4. Otherwise (fewer than 4 stories OR only 1 parallel group) → invoke a single task-executor agent per story

**TDD enforcement** (applies to both team and sequential):
- For each acceptance criterion: RED (failing test) → GREEN (minimum code) → REFACTOR
- Never write production code without a failing test first
- See `test-driven-development` skill

**Post-story validation** (applies to both team and sequential):
- After each story, run the `task-validation-loop` skill (3 checkers)
- architecture-alignment-checker, design-consistency-checker, prd-architecture-checker
- All must pass before proceeding to next story

After implementation:
- Run `python3 .claude/linters/lint_all.py` — all linters must pass
- Run `pytest tests/ --cov=src --cov-fail-under=80` — all tests must pass

**Gate**: All linters pass, all tests pass, coverage >= 80%, all task-validation-loops passed

### Phase 7: Test Fill

**Agent**: test-writer
**Trigger**: Coverage is below 80% or acceptance criteria lack test coverage
**Output**: Additional tests in `tests/`
**Skip**: If coverage >= 80% and all acceptance criteria have tests

**Gate**: Coverage >= 80%, all acceptance criteria covered

### Phase 8: E2E Tests

**Agent**: e2e-writer
**Input**: Test plan E2E section + design doc API contracts
**Output**: `tests/e2e/` with Playwright browser tests or httpx API tests

**Gate**: E2E test files exist, `pytest tests/e2e/ -m e2e` passes

### Phase 9: DevOps

**Agent**: devops
**Input**: App spec infrastructure section
**Output**: `infra/`, `.github/workflows/deploy.yml`, updated Dockerfile/docker-compose/Makefile

**Gate**: Infrastructure files exist, Dockerfile builds (if Docker available)

### Phase 10: Review (8-Agent Validation Loop)

**Skill**: `validation-loop` — runs 8 reviewers in parallel

**Gating reviewers** (5 — must all APPROVE unanimously):
1. **spec-reviewer** — does the implementation match the spec?
2. **code-reviewer** — is the code quality acceptable?
3. **security-reviewer** — is the code secure?
4. **performance-reviewer** — are there performance issues?
5. **architecture-alignment-checker** — does code align with architecture docs?

**Advisory reviewers** (3 — inform but don't block):
6. **design-consistency-checker** — does UI comply with design system?
7. **code-simplifier** — is there over-engineering?
8. **prd-architecture-checker** — do architecture docs match requirements?

All 8 run in parallel. If any gating reviewer returns REQUEST_CHANGES:
1. Collect all findings from failing gating reviewers
2. Re-invoke implementer with combined findings
3. Re-run only failing gating reviewers
4. Max 3 cycles. If still failing, escalate to user.

**Gate**: All 5 gating reviewers pass unanimously

### APPROVAL CHECKPOINT 2

**Action**: Present the review results and a summary of all changes to the user.
**Show**: Review verdicts, files changed, test results, coverage report.
**Wait**: Do NOT proceed until the user approves.

### Phase 11: PR

**Agent**: pr-writer
**Input**: All changes, spec, stories, review verdicts
**Output**: Pull request with story-based commits

**Gate**: PR created successfully

## Team Orchestration Protocol (Claude Code Agent Teams)

> Agent teams are experimental. Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json.

**MUST** use teams when: **4+ stories AND 2+ parallel groups** in the stories file. This is a mechanical check — count the stories and groups, then follow the rule. Do not substitute your own judgment about whether stories are "too small" or "mostly sequential."

Each teammate is a **full, independent Claude Code session** with its own context window. Teammates coordinate through a shared task list and direct messaging (SendMessage). Unlike subagents, teammates can message each other directly.

### Setup (via `teams` skill)

The `teams` skill handles the full team lifecycle:

1. Create a feature branch: `git checkout -b feat/<feature-name>`
2. **TeamCreate** — creates team and shared task list:
   ```
   TeamCreate(team_name="feat-<feature-name>", description="Implementing <feature>")
   ```
   Creates: `~/.claude/teams/feat-<feature-name>/config.json` + `~/.claude/tasks/feat-<feature-name>/`

3. **TaskCreate** — one task per story with dependency blocking:
   ```
   TaskCreate(
     subject="US-XXX: <title>",
     description="<story text + acceptance criteria + file ownership>",
     activeForm="Implementing US-XXX"
   )
   TaskUpdate(taskId=<id>, addBlockedBy=[<dependency-ids>])
   ```
   File ownership is assigned per task to avoid conflicts between teammates.

4. **Spawn teammates** — one per parallel group:
   ```
   Task(
     subagent_type="general-purpose",
     team_name="feat-<feature-name>",
     name="implementer-group-<N>",
     mode="bypassPermissions",
     prompt="You are an implementer teammate. Follow .claude/agents/task-executor.md for TDD.
       Self-claim tasks from TaskList, implement with TDD, validate, commit, report via SendMessage.
       Only modify files in your task description."
   )
   ```
   Each teammate loads CLAUDE.md, MCP servers, and skills automatically — but NOT the lead's conversation history.

5. **Monitor** — teammates send automatic idle notifications. The lead monitors via:
   - `TaskList` — poll task statuses
   - `SendMessage` notifications from teammates on task completion
   - Direct interaction via Shift+Down (in-process mode) or clicking panes (tmux mode)

6. **Verify** after all tasks complete:
   ```
   pytest tests/ --cov=src --cov-fail-under=80
   python3 .claude/linters/lint_all.py
   ```

7. **Graceful shutdown** — always in this order:
   ```
   For each teammate:
     SendMessage(type="shutdown_request", recipient="<name>", content="All tasks complete.")
   Wait for all shutdown_response(approve=True)
   TeamDelete  # Only the lead runs this!
   ```

### Quality Gate Hooks

Two hooks enforce quality automatically:
- **TeammateIdle**: checks for incomplete tasks before allowing idle (exit 2 to keep working)
- **TaskCompleted**: runs linters and tests before allowing task completion (exit 2 to reject)

### Sequential Fallback

Use sequential implementation (single implementer agent) **only** when:
- Fewer than 4 stories, OR
- Only 1 parallel group (all stories form a single dependency chain), OR
- Team setup fails (after attempting team orchestration first)

**Common mistake**: An agent may rationalize skipping teams by saying stories are "small" or "mostly sequential." This is not a valid reason. The threshold is purely mechanical: count stories, count parallel groups. If both thresholds are met, use teams.

## Error Recovery

| Error | Recovery |
|-------|----------|
| Spec-writer didn't produce all artifacts | Re-invoke spec-writer for missing phases only |
| Implementation fails linters | Read error, fix code, re-run linters |
| Tests fail | Read failures, fix code, re-run tests |
| Coverage below 80% | Invoke test-writer agent |
| Review fails | Re-invoke implementer with review feedback, re-review |
| E2E tests fail | Read failures, fix tests or code, re-run |
| Docker build fails | Fix Dockerfile, re-build |
