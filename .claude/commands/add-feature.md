---
disable-model-invocation: true
---

# /forge:add-feature

Feature SDLC pipeline for adding a feature to an existing application. Like `/forge:build` but skips the app-level spec and starts with a feature spec interview.

## When to Use

Use this command when adding a new feature to an already-scaffolded project. The project must have an existing `src/` directory and `CLAUDE.md`. If the project has not been initialized, use `/forge:init` first.

## Arguments

- **description** (required): A natural-language description of the feature to add. Everything after `/forge:add-feature` is treated as the description.

Example: `/forge:add-feature add team-based permissions with role management`

## Process

This command triggers the **full pipeline** starting from Phase 1 (skipping Phase 0 app spec). All remaining phases execute automatically with human approval checkpoints.

### Phase 1: Feature Spec (Socratic Interview)
1. Invoke the **spec-writer** agent in **feature mode**.
2. The spec-writer conducts a focused interview about the feature — scope, user impact, integration points with existing code, constraints.
3. The spec-writer scans the existing codebase to understand current architecture and avoid conflicts.
4. Output: `specs/features/<feature-name>_spec.md`

### Phase 2: User Stories
5. Spec-writer generates user stories scoped to the feature.
6. Output: `specs/stories/US-XXX.md` (numbering continues from existing stories)

### Phase 3: Design Document
7. Generate design document showing how the feature integrates with existing architecture.
8. Output: `specs/design/<feature-name>_design.md`

### Phase 4: Test Plan
9. Generate test plan for the feature.
10. Output: `specs/tests/<feature-name>_test_plan.md`

### Phase 5: Execution Plan
11. Generate implementation plan with story ordering and parallel groups.
12. Output: `specs/plans/<feature-name>_execution_plan.md`

### CHECKPOINT 1: Human Approval
13. Present all artifacts to the user.
14. **Wait for explicit approval** before proceeding.

### Phase 6: Implementation
15. Count stories and parallel groups from the execution plan.
16. **If 4+ stories AND 2+ parallel groups**: Create a team with implementer agents per parallel group.
17. **Otherwise**: Invoke a single implementer agent sequentially.
18. Run `python3 .claude/linters/lint_all.py` and `make test` after each story.

### Phase 7: Test Fill
19. Invoke **test-writer** agent to fill coverage gaps.

### Phase 8: E2E Tests
20. Invoke **e2e-writer** agent for feature-specific E2E tests.

### Phase 9: DevOps
21. Invoke **devops** agent to update CI/CD if needed for the new feature.

### Phase 10: Three-Stage Review
22. Run spec-reviewer, code-reviewer, and security-reviewer with retry loops (max 3 cycles each).

### CHECKPOINT 2: Human Approval
23. Present review results. **Wait for approval.**

### Phase 11: PR Creation
24. Invoke **pr-writer** agent for a structured PR.

### Throughout All Phases
- Update `specs/pipeline_status.md` after each phase.
- Verify artifacts before advancing.
