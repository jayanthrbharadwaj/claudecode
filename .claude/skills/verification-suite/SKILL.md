---
description: "Three-tier verification system: gating reviews, advisory checks, and per-story feedback"
disable-model-invocation: true
---

# Verification Suite

A merged verification system with three tiers: gating (blocks PR), advisory (informational), and per-story (feedback loop to implementer).

## Tier 1: Gating Reviews (Blocks PR)

All 5 gating reviewers must pass unanimously before a PR can be created. All 8 reviewers (5 gating + 3 advisory) run in parallel. Each gating reviewer has a max retry cycle of 3.

### Gating Reviewers (5 — must all APPROVE)

#### 1. Spec Review

**Agent**: spec-reviewer (via Task tool, in parallel)
**Question**: Does the implementation match the spec?

**Checks**:
- Every acceptance criterion in the spec has corresponding implementation
- API endpoints match the spec (paths, methods, request/response formats)
- Data model matches the spec (fields, types, constraints)
- Business rules are correctly implemented
- Edge cases from the spec are handled

#### 2. Code Review

**Agent**: code-reviewer (via Task tool, in parallel)
**Question**: Is code quality acceptable?

**Checks**:
- Naming conventions (snake_case, PascalCase as appropriate)
- File and function size limits (300 lines/file, 50 lines/function)
- Type annotations on all functions
- Structured logging (no print statements)
- Error handling (specific exceptions, context in logs)
- Import ordering (stdlib -> third-party -> project in layer order)
- No dead code, no commented-out code

#### 3. Security Review

**Agent**: security-reviewer (via Task tool, in parallel)
**Question**: Is the code secure?

**Checks**:
- OWASP Top 10 vulnerabilities
- Auth flows: token validation, session handling, permission checks
- Secrets: no hardcoded credentials, API keys, or tokens
- Input validation at system boundaries
- Dependency vulnerabilities

#### 4. Performance Review

**Agent**: performance-reviewer (via Task tool, in parallel)
**Question**: Are there performance issues?

**Checks**:
- N+1 queries (loop with individual DB calls)
- Unbounded loops that grow with user data
- Missing pagination on list endpoints
- Blocking I/O in async contexts
- Missing connection pooling
- Caching opportunities for repeated queries

#### 5. Architecture Alignment

**Agent**: architecture-alignment-checker (via Task tool, in parallel)
**Question**: Does code align with architecture docs?

**Checks**:
- Layer placement (Types, Config, Repo, Service, Runtime, UI)
- Dependency direction (forward-only, no backward imports)
- Service has no direct I/O
- Module structure matches design doc
- Cross-cutting concerns follow documented patterns

### Advisory Reviewers (3 — inform but don't block)

#### 6. Design Consistency

**Agent**: design-consistency-checker (via Task tool, in parallel)
**Question**: Does UI comply with design system?
**Note**: Advisory only — findings are included in the report but never block the PR.

#### 7. Code Simplifier

**Agent**: code-simplifier (via Task tool, in parallel)
**Question**: Is there over-engineering?
**Note**: Advisory only — suggests simplifications but never blocks.

#### 8. PRD-Architecture Alignment

**Agent**: prd-architecture-checker (via Task tool, in parallel)
**Question**: Do architecture docs match product requirements?
**Note**: Advisory only — flags gaps between requirements and architecture.

### Review Execution

All 8 reviewers are invoked in parallel via the Task tool. This replaces the previous sequential 3-reviewer pattern.

**On FAIL** (any gating reviewer returns REQUEST_CHANGES):
1. Collect all findings from failing gating reviewers
2. Re-invoke implementer agent with the combined findings list
3. After implementer fixes, re-run ONLY the failing gating reviewers
4. Max 3 cycles. If still failing, escalate to user.

**Verdict format**:
```
PASS | FAIL
Issues: [list of specific discrepancies with file:line references]
```

---

## Tier 2: Advisory Checks (Informational)

These checks produce reports but do not block the PR. Results are included in the PR description for visibility.

### Test Coverage

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

Report includes:
- Overall coverage percentage
- Per-file coverage with uncovered lines
- Comparison against 80% threshold

### Linter Check

```bash
python3 .claude/linters/lint_all.py
```

Report includes:
- Layer dependency violations
- File size violations
- Any other configured linter results

### Dependency Audit

Check for known CVEs in project dependencies:

```bash
# Python
pip-audit --strict

# Node.js
npm audit --audit-level=moderate
```

Report includes:
- Number of vulnerabilities by severity
- Affected packages and recommended fixes

### Documentation

Check that public APIs have docstrings:
- All service functions in `src/service/`
- All route handlers in `src/ui/`
- All Pydantic models in `src/types/`

### Deployment Readiness

- Dockerfile builds successfully (if present)
- CI workflow syntax is valid
- Required environment variables are documented in `.env.example`

---

## Tier 3: Per-Story Feedback (To Implementer)

These checks run after each story is implemented and provide immediate feedback to the implementer agent before moving to the next story.

### Story Completion

For the implemented story, verify:
- All acceptance criteria from the story have corresponding code
- All acceptance criteria have at least one test with a spec reference comment
- No acceptance criteria are partially implemented

### Test Meaningfulness

Check tests written for this story:
- No vacuous assertions (`assert result is not None`, `assert response`, `assert len(items) > 0`)
- Every assertion verifies specific behavior: exact values, exception types, or state changes
- Test names follow the pattern: `test_<function>_<scenario>_<expected_outcome>`

### Layer Compliance

Check code written for this story:
- All imports follow the forward-only direction rule
- No backward imports introduced
- New types are in `src/types/`, not inline in higher layers

---

## Invocation

This skill is invoked by:
- `/forge:review` -- runs Tier 1 (8 parallel reviewers: 5 gating + 3 advisory) + Tier 2 (advisory) and produces a combined report
- Phase 10 of the SDLC pipeline -- runs the `validation-loop` skill (8 parallel reviewers) automatically
- Per-story checks during Phase 6 (implementation) -- runs the `task-validation-loop` skill (3 checkers) automatically

## Output

Combined verification report saved to `specs/review_report.md`:

```markdown
# Verification Report
Generated: <timestamp>

## Tier 1: Gating Reviews
| Reviewer | Verdict | Cycles | Notes |
|----------|---------|--------|-------|
| Spec     | PASS    | 1      | All 8 criteria matched |
| Code     | PASS    | 2      | Fixed naming issues in cycle 1 |
| Security | PASS    | 1      | No issues found |
| Performance | PASS | 1      | No N+1 queries |
| Architecture | PASS | 1     | All layers correct |
| Design (advisory) | 2 suggestions | - | Minor spacing |
| Simplifier (advisory) | 1 suggestion | - | Factory could be simpler |
| PRD-Arch (advisory) | ALIGNED | - | All requirements covered |

## Tier 2: Advisory
| Check | Result | Details |
|-------|--------|---------|
| Coverage | 87% | 3 files below 80% |
| Linters | PASS | No violations |
| Dependencies | 0 CVEs | All clear |
| Docs | 2 missing | src/service/auth.py, src/service/search.py |
| Deploy | PASS | Dockerfile builds |

## Tier 3: Per-Story (last run)
| Story | Completion | Tests | Layers |
|-------|-----------|-------|--------|
| US-001 | 5/5 criteria | PASS | PASS |
| US-002 | 4/4 criteria | PASS | PASS |
```
