---
disable-model-invocation: true
---

# /forge:build-unplanned

Build a feature with a lightweight brief but no full spec pipeline.

## When to Use

- You want more structure than `/forge:just-do-it` but less than `/forge:build`
- The feature is medium complexity — needs a brief but not a full spec/stories/design cycle
- You want TDD enforcement and validation but not the full review loop

## Arguments

- **description** (required): What to build, in plain language

## Process

1. Invoke the `build-unplanned-feature` skill with the user's description
2. The skill generates a lightweight feature brief (not a full spec)
3. Implementation follows TDD: failing test → minimum code → refactor
4. Post-implementation runs the task-validation-loop (3 checkers)
5. If validation passes, commit and present results
6. If validation fails, fix and retry (max 3 cycles)
