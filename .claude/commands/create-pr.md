---
disable-model-invocation: true
---

# /forge:create-pr

Create a structured pull request with story-based commits. Verifies that reviews have passed before proceeding.

## When to Use

Use this command after implementation and reviews are complete. This is typically the final step in the pipeline. Requires that `/forge:review` (or the review phase in `/forge:build`) has passed all three gating stages.

## Arguments

- **--base** (optional): The base branch to target. Defaults to `main`.
- **--draft** (optional): If provided, creates the PR as a draft.

Examples:
- `/forge:create-pr`
- `/forge:create-pr --base develop --draft`

## Process

### Pre-flight Checks

1. **Verify reviews have passed**:
   - Check `specs/pipeline_status.md` for review phase status.
   - If reviews have not passed, inform the user:
     > "Reviews have not passed yet. Run `/forge:review` first."
   - Stop if reviews are incomplete.

2. **Verify tests pass**:
   - Run `make test` to confirm all tests pass.
   - If tests fail, report the failures and stop.

3. **Verify linters pass**:
   - Run `python3 .claude/linters/lint_all.py`.
   - If linters fail, report violations and stop.

### PR Creation

4. Invoke the **pr-writer** agent with the following context:
   - All story files from `specs/stories/`
   - The spec from `specs/features/`
   - The design document from `specs/design/`
   - The current git log and diff

5. The pr-writer agent:
   a. Organizes commits by story — each story gets its own commit with format `feat(US-XXX): description`.
   b. Squashes or reorganizes commits if needed for a clean history.
   c. Writes the PR title (under 70 characters) and body with:
      - Summary section (what was built and why)
      - Stories covered (list of US-XXX with descriptions)
      - Design decisions (key architectural choices)
      - Test plan (how to verify)
      - Breaking changes (if any)

6. **Push to remote**:
   - Ensure the current branch is pushed with `git push -u origin <branch>`.

7. **Create the PR**:
   ```
   gh pr create --title "<title>" --body "<body>" --base <base-branch>
   ```
   - Add `--draft` flag if the user requested a draft PR.

8. **Report the PR URL** to the user.

9. **Update `specs/pipeline_status.md`** to mark the PR phase as complete.
