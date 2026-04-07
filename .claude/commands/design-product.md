---
disable-model-invocation: true
---

# /forge:design-product

Run the spec-writer interview to produce a product spec without triggering implementation.

## When to Use

- You want to design a feature spec without building it yet
- You want to iterate on requirements before committing to implementation
- Same as `/forge:design` but named for clarity alongside `/forge:design-architecture`

## Arguments

- **description** (required): What feature to design

## Process

1. Invoke the spec-writer agent via Task tool
2. Spec-writer conducts the Socratic interview
3. Produces: spec, stories, design doc, test plan, execution plan
4. All artifacts saved to `specs/` directories
5. Does NOT proceed to implementation — stops after the execution plan
6. User can later run `/forge:resume` to continue the pipeline
