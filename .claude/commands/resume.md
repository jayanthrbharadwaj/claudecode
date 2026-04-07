---
disable-model-invocation: true
---

# /forge:resume

Resume an in-progress SDLC pipeline from the last completed phase.

## When to Use

Use this command to continue a pipeline that was interrupted — for example, after a session timeout, context limit, or manual pause. Also use it when returning to a project after reviewing artifacts produced in a previous session.

## Arguments

None. The command reads pipeline state from `specs/pipeline_status.md`.

## Process

1. **Check for pipeline status file** at `specs/pipeline_status.md`.
   - If the file does **not** exist, inform the user:
     > "No pipeline in progress. Use `/forge:build` to start a new application or `/forge:add-feature` to add a feature."
   - Stop here if no status file exists.

2. **Read `specs/pipeline_status.md`** and parse the phase statuses.

3. **Identify the last completed phase** and determine the next phase to execute.

4. **Verify artifacts** for all completed phases — confirm the expected output files exist at their paths. If any completed phase is missing its artifacts, flag this to the user and ask whether to re-run that phase or skip.

5. **Report current state** to the user:
   - List completed phases with their artifacts
   - Show the next phase to execute
   - Show any blocked or failed phases

6. **Resume execution** from the next incomplete phase, following the same process as `/forge:build` or `/forge:add-feature` (depending on what initiated the pipeline).

7. Continue through all remaining phases, respecting human approval checkpoints.

8. Update `specs/pipeline_status.md` after each phase completes.
