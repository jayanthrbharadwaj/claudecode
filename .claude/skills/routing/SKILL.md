---
description: "Dual-mode request classifier and router. Matches: build, create, add feature, continue, resume, scaffold, new app, new feature, what's next, I want an app"
disable-model-invocation: true
---

# Request Router

Classifies incoming requests and routes them to the correct skill or workflow.

## Classification

When loaded, classify the user's request into one of three categories and take the corresponding action.

### Category A: Pipeline Trigger

**Matches**: "build me", "create a", "I want an app that", "add feature X", "build X feature", "add X to the app", "new app", "new feature", "scaffold"

**Action**: Invoke the `sdlc-pipeline` skill using the Skill tool:

```
Skill: forge:sdlc-pipeline
Args: <user's original request>
```

This starts the full SDLC pipeline beginning with the spec-writer interview. Do NOT explore the codebase, research, or plan first. The pipeline handles everything.

### Category A-bis: Quick Build

**Matches**: "just do it", "just build", "quick change", "quickly add", "don't need a spec", "skip the spec", "no ceremony"

**Action**: Invoke the `build-unplanned-feature` skill using the Skill tool:

```
Skill: forge:build-unplanned-feature
Args: <user's original request>
```

This builds the feature with TDD but without full spec ceremony. Lighter than the full pipeline.

### Category B: Resume Pipeline

**Matches**: "continue", "resume", "what's next", "continue the pipeline", "keep going"

**Action**:

1. Read `specs/pipeline_status.md`
2. Find the last completed phase
3. Resume from the next incomplete phase by invoking `forge:sdlc-pipeline` with the resume context
4. If `specs/pipeline_status.md` does not exist, tell the user there is no active pipeline and suggest `/forge:build` or `/forge:add-feature`

### Category C: Toolbox (No routing needed)

**Matches**: Everything else (bug fixes, refactoring, questions, direct edits)

**Action**: No routing action needed. Individual `/forge:*` commands are available for targeted tasks:

**Pipeline & Build**:
- `/forge:build` — full pipeline for greenfield apps
- `/forge:add-feature` — pipeline for adding a feature
- `/forge:just-do-it` — quick build without spec ceremony
- `/forge:build-unplanned` — lightweight build with brief
- `/forge:resume` — resume from last checkpoint

**Design & Architecture**:
- `/forge:design` — spec interview only
- `/forge:design-product` — product spec design workflow
- `/forge:design-architecture` — architecture design workflow

**Implementation**:
- `/forge:work-on` — work on a specific task/story (TDD)
- `/forge:work-on-next` — pick next story, implement
- `/forge:create-tasks` — create tasks from stories

**Quality & Validation**:
- `/forge:review` — 8-agent parallel gating review
- `/forge:validate` — full verification suite
- `/forge:check` — 3-dimension alignment checks

**Reverse Engineering**:
- `/forge:source-architecture` — architecture docs from code
- `/forge:source-specs` — specs from existing code
- `/forge:spec-sync` — bidirectional spec-code sync

**Utilities**:
- `/forge:init` — scaffold a new project
- `/forge:debug` — 5-phase debugging workflow
- `/forge:refactor` — targeted debt reduction
- `/forge:create-pr` — structured PR with story commits
- `/forge:skills` — list all available skills
- `/forge:help` — show all commands, skills, agents

Let the user proceed with their request. Quality gates (linters, tests) activate automatically on code changes.

## Classification Rules

- If the request is ambiguous between Category A and C (e.g., "add validation to the login form"), prefer Category C. Category A requires explicit feature-building language.
- If the user says "build" or "create" referring to a specific small fix, not a feature, classify as Category C.
- If the request matches Category A-bis ("just do it", "quick change"), route to `build-unplanned-feature` instead of the full pipeline.
- When in doubt, ask: "Are you asking me to build a new feature (which starts the full pipeline), make a quick change (TDD only), or make a direct edit?"
