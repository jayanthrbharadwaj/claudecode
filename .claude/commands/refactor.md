---
disable-model-invocation: true
---

# /forge:refactor

Targeted code debt reduction. Finds violations, prioritizes fixes, and refactors one file at a time with test verification.

## When to Use

Use this command when code quality has degraded and needs cleanup. Common scenarios:
- After rapid feature development
- When linters report persistent violations
- When file sizes exceed limits
- When architecture layer boundaries have been violated
- General code hygiene and debt reduction

## Arguments

- **target** (optional): A specific file, directory, or area to focus on. If omitted, the refactorer scans the entire `src/` directory.

Examples:
- `/forge:refactor` — scan and fix across the whole codebase
- `/forge:refactor src/service/` — focus on the service layer
- `/forge:refactor src/repo/user_repo.py` — refactor a specific file

## Process

### 1. Discover Violations

1. Run `python3 .claude/linters/lint_all.py` to get the current violation report.
2. Invoke the **refactorer** agent to analyze the codebase for:
   - Layer dependency violations (backward imports)
   - Files exceeding 300-line limit
   - Functions exceeding 50-line limit
   - Naming convention violations (`snake_case` files/functions, `PascalCase` classes)
   - Code duplication across modules
   - Missing or incorrect type annotations for domain concepts
   - Raw `print()` or `console.log()` instead of structured logging

### 2. Prioritize

3. Rank violations by severity:
   - **Critical**: Layer dependency violations (breaks architecture)
   - **High**: File/function size violations (blocks CI)
   - **Medium**: Naming and convention violations
   - **Low**: Code duplication and style improvements

4. Present the prioritized list to the user with estimated scope per fix.

### 3. Refactor (One File at a Time)

5. For each file, starting with the highest priority violation:
   a. Read the file and understand its purpose and dependencies.
   b. Apply the minimal refactoring needed to fix the violation.
   c. If splitting a file, ensure the new files follow the naming conventions and layer rules.
   d. Update all imports that reference the refactored file.
   e. Run `python3 .claude/linters/lint_all.py` to verify the violation is fixed.
   f. Run `make test` to verify no tests broke.
   g. If tests fail, fix the test or revert the refactoring and try a different approach.

6. After each file is successfully refactored, report what changed.

### 4. Final Report

7. Summarize all refactoring performed:
   - Files modified
   - Violations fixed (by category)
   - Remaining violations (if any)
   - Test status after all changes
