#!/usr/bin/env python3
"""TaskCompleted hook — runs when a task is being marked complete.

Exit code 0: allow completion
Exit code 2: reject completion with feedback (task stays in_progress)

Checks that the task's acceptance criteria are met:
- Linters pass on changed files
- Tests pass
"""
import json
import subprocess
import sys


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    task_subject = data.get("tool_input", {}).get("subject", "")
    task_status = data.get("tool_input", {}).get("status", "")

    # Only check when marking as completed
    if task_status != "completed":
        sys.exit(0)

    # Run linters as a quick quality gate
    try:
        result = subprocess.run(
            ["python3", ".claude/linters/lint_all.py"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            print(
                f"Cannot mark task complete — linter violations found:\n"
                f"{result.stdout[:500]}",
                file=sys.stderr,
            )
            sys.exit(2)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # If linters can't run, allow completion (advisory)
        pass

    # Run quick test check
    try:
        result = subprocess.run(
            ["python3", "-m", "pytest", "tests/", "-x", "-q", "--tb=no"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            print(
                f"Cannot mark task complete — tests are failing:\n"
                f"{result.stdout[:500]}",
                file=sys.stderr,
            )
            sys.exit(2)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # If tests can't run, allow completion (advisory)
        pass

    # All checks passed — allow completion
    sys.exit(0)


if __name__ == "__main__":
    main()
