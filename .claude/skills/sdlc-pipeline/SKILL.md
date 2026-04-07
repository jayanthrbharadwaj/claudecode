---
description: "Full 11-phase SDLC pipeline orchestration from spec through PR"
disable-model-invocation: true
---

# SDLC Pipeline

Orchestrates the complete software development lifecycle in 11 phases with two human approval checkpoints.

## Pipeline Phases

```
1. Spec --> 2. Stories --> 3. Design --> 4. Test Plan --> 5. Exec Plan
--> [APPROVE] -->
6. Implement --> 7. Test Fill --> 8. E2E Tests --> 9. DevOps
--> 10. Review --> [APPROVE] --> 11. PR
```

## Phase Gate Protocol

Before advancing from any phase to the next:

1. **Verify artifacts exist** at expected paths (see each phase below)
2. **Update `specs/pipeline_status.md`** — mark current phase complete with timestamp
3. If `specs/pipeline_status.md` does not exist, copy from `.claude/templates/pipeline_status.md` and fill in the feature name

## Cross-Turn Resumption

When resuming a pipeline (user says "continue", "resume", "what's next"):

1. Read `specs/pipeline_status.md`
2. Find the last completed phase
3. Resume from the next incomplete phase
4. If no `pipeline_status.md` exists, inform the user and suggest starting fresh

---

## Phase 1: Spec

**Agent**: spec-writer (via Task tool)
**Trigger**: User says "Build me X" or "Add feature X"
**Scope detection**:
- Greenfield ("Build me X", "Create a X app") -> spec-writer runs Phase 0 (App Spec) then decomposes into feature specs
- Feature addition ("Add feature X") -> spec-writer runs Phase 1 (Feature Interview) directly

**Prompt for spec-writer agent**:
> You are the spec-writer agent. Read your instructions from `.claude/agents/spec-writer.md`. The user wants: [USER REQUEST]. Conduct the Socratic interview, produce the spec, and continue through stories, design, test plan, and execution plan.

**Output (greenfield)**: `specs/app_spec.md` + `specs/features/*.md`
**Output (feature)**: `specs/features/<feature-name>.md`
**Gate**: Spec file(s) exist and user has reviewed them

**Error recovery**: If spec-writer does not produce all artifacts, re-invoke for missing phases only.

## Phase 2: Stories

**Agent**: spec-writer (continues from Phase 1)
**Output**: `specs/stories/<feature-name>.md`
**Gate**: Stories file exists with dependency graph and parallel groups

**Error recovery**: Re-invoke spec-writer with the approved spec and ask for story decomposition only.

## Phase 3: Design

**Agent**: spec-writer (continues)
**Output**: `specs/design/<feature-name>.md`
**Gate**: Design doc exists with layer impact analysis, API contracts, and sequence diagrams

**Error recovery**: Re-invoke spec-writer with spec + stories, ask for design doc only.

## Phase 4: Test Plan

**Agent**: spec-writer (continues)
**Output**: `specs/tests/<feature-name>.md`
**Gate**: Test plan exists with test cases (TC-XXX), test types, concrete test data

**Error recovery**: Re-invoke spec-writer with spec + stories + design, ask for test plan only.

## Phase 5: Execution Plan

**Agent**: spec-writer (continues)
**Output**: `specs/plans/<feature-name>.md`
**Gate**: Execution plan exists with tasks, file paths, story ordering, and parallel groups

**Error recovery**: Re-invoke spec-writer with all prior artifacts, ask for execution plan only.

---

## APPROVAL CHECKPOINT 1

**Action**: Present the following to the user:
- Summary of the spec (1-2 sentences)
- List of user stories with IDs
- Key design decisions
- Test coverage overview
- Implementation plan with story ordering

**Wait**: Do NOT proceed until the user says "approved", "go ahead", "looks good", "LGTM", or similar affirmative.

**If user requests changes**: Loop back to the relevant phase (spec, stories, design, etc.) and re-run from there.

---

## Phase 6: Implement

**Agent**: implementer (or team of implementers via `teams` skill)
**Input**: Spec, stories, design, execution plan
**TDD**: Mandatory — every acceptance criterion follows RED → GREEN → REFACTOR cycle (see `test-driven-development` skill)

### Team Orchestration Check (MANDATORY)

This is a mechanical check. Do NOT skip it or override it based on judgment.

1. Read the stories file and count the total number of stories
2. Count the number of parallel groups in the "Parallel Groups" section
3. Apply the rule:

| Stories | Parallel Groups | Action |
|---------|----------------|--------|
| >= 4    | >= 2           | **MUST use `teams` skill** for parallel implementation |
| < 4     | any            | Single task-executor agent |
| any     | < 2            | Single task-executor agent |

### Team Implementation (via `teams` skill)

When teams are required, invoke the `teams` skill which handles the full lifecycle:

1. **TeamCreate** — create team `feat-<feature-name>`
2. **TaskCreate** — one task per story with `addBlockedBy` from dependency graph
3. **Task (spawn agents)** — one implementer agent per parallel group, each using TDD enforcement
4. **Monitor** — track progress via TaskList and SendMessage notifications
5. **Verify** — run full test suite after all tasks complete
6. **Cleanup** — shutdown agents, TeamDelete

Each implementer agent:
- Follows TDD for every acceptance criterion (RED → GREEN → REFACTOR)
- Runs task-validation-loop after each story (3 checkers)
- Commits per story: `feat(US-XXX): description`
- Reports completion via SendMessage

### Sequential Implementation

When teams are not required:

1. Invoke a single task-executor agent with each story in dependency order
2. Each story follows TDD enforcement
3. Each story runs task-validation-loop after completion
4. Commit per story: `feat(US-XXX): description`

**Post-implementation**:
- Run `python3 .claude/linters/lint_all.py` (all linters must pass)
- Run `pytest tests/ --cov=src --cov-fail-under=80` (all tests must pass)

**Gate**: All linters pass, all tests pass, coverage >= 80%, all task-validation-loops passed

**Error recovery**:
- Linter failures: read the error (it contains the fix), fix code, re-run
- Test failures: read failures, fix code, re-run
- Coverage below 80%: proceed to Phase 7 (Test Fill)
- Task-validation failures: fix and retry (max 3 cycles per story)

## Phase 7: Test Fill

**Agent**: test-writer
**Trigger**: Coverage < 80% or acceptance criteria lack test coverage
**Skip condition**: Coverage >= 80% AND all acceptance criteria have corresponding tests

**Prompt for test-writer agent**:
> You are the test-writer agent. Read your instructions from `.claude/agents/test-writer.md`. Fill coverage gaps to reach 80%+. The test plan is at `specs/tests/<feature-name>.md`. Focus on untested acceptance criteria first, then branch coverage.

**Output**: Additional tests in `tests/`
**Gate**: `pytest --cov=src --cov-fail-under=80` passes, all acceptance criteria have tests

**Error recovery**: Re-invoke test-writer with the coverage report showing gaps.

## Phase 8: E2E Tests

**Agent**: e2e-writer
**Input**: Test plan E2E section + design doc API contracts

**Prompt for e2e-writer agent**:
> You are the e2e-writer agent. Read your instructions from `.claude/agents/e2e-writer.md`. Create E2E tests from the test plan at `specs/tests/<feature-name>.md` and the API contracts in `specs/design/<feature-name>.md`.

**Output**: `tests/e2e/` with Playwright browser tests or httpx API tests
**Gate**: E2E test files exist, `pytest tests/e2e/ -m e2e` passes

**Error recovery**: Read test failures, fix tests or implementation code, re-run.

## Phase 9: DevOps

**Agent**: devops
**Input**: App spec infrastructure section, existing CI/CD config

**Prompt for devops agent**:
> You are the devops agent. Read your instructions from `.claude/agents/devops.md`. Create or update CI/CD pipeline, deployment configs, and infrastructure-as-code based on the app spec.

**Output**: `infra/`, `.github/workflows/`, updated Dockerfile/docker-compose/Makefile
**Gate**: Infrastructure files exist, Dockerfile builds (if Docker is available)

**Error recovery**: Fix Dockerfile or CI config, re-build, re-run.

---

## Phase 10: Review (8-Agent Validation Loop)

Invoke the `validation-loop` skill which runs 8 reviewers in parallel with unanimous approval.

### Gating Reviewers (5 — must all APPROVE)

| # | Agent | Question |
|---|-------|----------|
| 1 | spec-reviewer | Does the implementation match the spec? |
| 2 | code-reviewer | Is code quality acceptable? |
| 3 | security-reviewer | Is the code secure? |
| 4 | performance-reviewer | Are there performance issues? |
| 5 | architecture-alignment-checker | Does code align with architecture docs? |

### Advisory Reviewers (3 — inform but don't block)

| # | Agent | Question |
|---|-------|----------|
| 6 | design-consistency-checker | Does UI comply with design system? |
| 7 | code-simplifier | Is there over-engineering? |
| 8 | prd-architecture-checker | Do architecture docs match requirements? |

### Process

1. Invoke all 8 reviewers in parallel via Task tool
2. Collect verdicts: gating reviewers must all APPROVE
3. If any gating reviewer returns REQUEST_CHANGES:
   a. Re-invoke implementer with combined findings
   b. Re-run only failing reviewers
   c. Max 3 cycles
4. Advisory findings are included in the report but never block

**Gate**: All 5 gating reviewers pass unanimously.

**Error recovery**: If any gating reviewer still fails after 3 cycles, present the remaining issues to the user and ask how to proceed.

---

## APPROVAL CHECKPOINT 2

**Action**: Present to the user:
- Review verdicts (spec, code, security) with summaries
- List of files changed
- Test results and coverage report
- Any open issues from review cycles

**Wait**: Do NOT create the PR until the user explicitly approves.

---

## Phase 11: PR

**Agent**: pr-writer
**Input**: All changes, spec, stories, review verdicts

**Prompt for pr-writer agent**:
> You are the pr-writer agent. Read your instructions from `.claude/agents/pr-writer.md`. Create a pull request with story-based commits. Include the spec summary, story list, review verdicts, and test results in the PR description.

**Output**: Pull request created
**Gate**: PR URL returned successfully

**Error recovery**: If PR creation fails, check git state, ensure changes are committed, and retry.

---

## Pipeline Status Tracking

After each phase completes, update `specs/pipeline_status.md`:

```markdown
| Phase | Status | Timestamp | Notes |
|-------|--------|-----------|-------|
| 1. Spec | DONE | 2026-02-23T10:00:00 | specs/features/auth.md |
| 2. Stories | DONE | 2026-02-23T10:15:00 | 5 stories, 2 parallel groups |
| 3. Design | IN PROGRESS | | |
| ... | | | |
```
