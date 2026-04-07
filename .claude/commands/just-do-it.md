---
disable-model-invocation: true
---

# /forge:just-do-it

Build a feature without spec ceremony — TDD and quick validation only.

## When to Use

- You have a clear, small feature request and don't need the full 11-phase pipeline
- You want to skip the Socratic interview and go straight to implementation
- The feature is simple enough that a spec would be overhead

## Arguments

- **description** (required): What to build, in plain language

## Process

1. Invoke the `build-unplanned-feature` skill with the user's description
2. The skill handles: parse request → TDD implementation → quick validation → commit
3. No spec files are created — the feature description serves as the requirement
4. Post-implementation validation uses a reduced set of checkers (architecture-alignment, design-consistency, prd-architecture)
5. Present results to the user
