---
disable-model-invocation: true
---

# /forge:design

Run the spec-writer interview and produce all design artifacts without auto-continuing to implementation. For users who want to review, iterate, and refine the design before building.

## When to Use

Use this command when you want to explore and refine the design before committing to implementation. This is useful for:
- Complex projects that need multiple design iterations
- Teams that want to review specs before building
- Situations where you want to produce design artifacts for external review

After design is complete, use `/forge:resume` to continue to implementation.

## Arguments

- **description** (required): A natural-language description of what to design. Everything after `/forge:design` is treated as the description.
- **--feature**: If provided, runs in feature mode (skips app-level spec, scans existing codebase).

Examples:
- `/forge:design a real-time collaboration platform with CRDT sync`
- `/forge:design --feature add webhook notification system`

## Process

### Phase 0: App Spec or Feature Spec
1. Invoke the **spec-writer** agent.
2. If `--feature` flag is present, run in feature mode (scan existing codebase, produce feature-scoped spec).
3. Otherwise, run the full Socratic interview for an app-level spec.
4. Output: `specs/features/<name>_spec.md`

### Phase 1: User Stories
5. Generate user stories from the approved spec.
6. Output: `specs/stories/US-XXX.md` files

### Phase 2: Design Document
7. Generate architecture and design document.
8. Output: `specs/design/<name>_design.md`

### Phase 3: Test Plan
9. Generate test plan covering unit, integration, and E2E tests.
10. Output: `specs/tests/<name>_test_plan.md`

### Phase 4: Execution Plan
11. Generate implementation plan with story ordering and parallel groups.
12. Output: `specs/plans/<name>_execution_plan.md`

### After All Design Phases
13. Update `specs/pipeline_status.md` marking Phases 0-4 as complete and Phase 5 (Implementation) as pending.
14. Present a summary of all produced artifacts to the user.
15. **STOP here.** Do NOT auto-continue to implementation.
16. Inform the user:
    > "Design phase complete. Review the artifacts above. When ready to build, run `/forge:resume` to continue to implementation."
