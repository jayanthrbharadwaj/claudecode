---
disable-model-invocation: true
---

# /forge:build

Full SDLC pipeline for greenfield applications. Takes a high-level description and produces a complete, tested, reviewed application.

## When to Use

Use this command when starting a new application from scratch. The user provides a description like `/forge:build a todo app with user auth` and the pipeline handles everything from spec through to PR.

## Arguments

- **description** (required): A natural-language description of the application to build. Everything after `/forge:build` is treated as the description.

Example: `/forge:build a todo app with user authentication and team sharing`

## Process

This command triggers the **full pipeline** as defined in `.claude/docs/pipeline.md`. All 11 phases execute automatically with human approval checkpoints.

### Phase 0: App Spec (Socratic Interview)
1. Invoke the **spec-writer** agent in interview mode.
2. The spec-writer conducts a Socratic interview with the user — asking clarifying questions about scope, users, constraints, and requirements.
3. Output: `specs/features/app_spec.md`

### Phase 1: User Stories
4. Spec-writer generates user stories from the approved spec.
5. Output: `specs/stories/US-001.md`, `US-002.md`, etc.

### Phase 2: Design Document
6. Generate architecture and design document.
7. Output: `specs/design/design.md`

### Phase 3: Test Plan
8. Generate test plan covering unit, integration, and E2E tests.
9. Output: `specs/tests/test_plan.md`

### Phase 4: Execution Plan
10. Generate implementation plan with story ordering and parallel groups.
11. Output: `specs/plans/execution_plan.md`

### CHECKPOINT 1: Human Approval
12. Present the spec, stories, design, test plan, and execution plan to the user.
13. **Wait for explicit approval** before proceeding. Do NOT auto-continue.
14. If the user requests changes, loop back to the relevant phase.

### Phase 5: Implementation
15. Count stories and parallel groups from the execution plan.
16. **If 4+ stories AND 2+ parallel groups**: Create a team with implementer agents per parallel group.
17. **Otherwise**: Invoke a single implementer agent sequentially.
18. Each story is implemented layer-by-layer following the architecture.
19. Run `python3 .claude/linters/lint_all.py` and `make test` after each story.

### Phase 6: Test Fill
20. Invoke **test-writer** agent to fill coverage gaps to 80%+.

### Phase 7: E2E Tests
21. Invoke **e2e-writer** agent to create E2E and API contract tests.

### Phase 8: DevOps
22. Invoke **devops** agent to create CI/CD pipeline and deployment configs.

### Phase 9: Three-Stage Review
23. Run **spec-reviewer** — if FAIL, re-invoke implementer, re-review (max 3 cycles).
24. Run **code-reviewer** — if FAIL, re-invoke implementer, re-review (max 3 cycles).
25. Run **security-reviewer** — if FAIL, re-invoke implementer, re-review (max 3 cycles).

### CHECKPOINT 2: Human Approval
26. Present the review results and final state to the user.
27. **Wait for explicit approval** before creating the PR.

### Phase 10: PR Creation
28. Invoke **pr-writer** agent to create a structured PR with story-based commits.

### Throughout All Phases
- Update `specs/pipeline_status.md` after each phase completes.
- If `specs/pipeline_status.md` does not exist, copy from `.claude/templates/pipeline_status.md`.
- Verify artifacts exist at expected paths before advancing to the next phase.
