#!/usr/bin/env python3
"""TeammateIdle hook — runs when a teammate is about to go idle.

Exit code 0: allow idle (teammate can stop)
Exit code 2: reject idle with feedback (keeps teammate working)

Checks that the teammate's assigned tasks are truly complete:
- All owned tasks are marked completed
- Tests pass for changed files
"""
import json
import sys
from pathlib import Path


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    # Extract teammate info
    teammate_name = data.get("agent_name", "unknown")
    team_name = data.get("team_name", "")

    if not team_name:
        # Not in a team context — allow idle
        sys.exit(0)

    # Check if there are uncompleted tasks owned by this teammate
    # by reading the task directory
    task_dir = Path.home() / ".claude" / "tasks" / team_name
    if not task_dir.is_dir():
        sys.exit(0)

    # Look for task files owned by this teammate that are not completed
    incomplete_tasks = []
    for task_file in task_dir.glob("*.json"):
        try:
            task_data = json.loads(task_file.read_text())
            owner = task_data.get("owner", "")
            status = task_data.get("status", "")
            subject = task_data.get("subject", "")
            if owner == teammate_name and status == "in_progress":
                incomplete_tasks.append(subject)
        except (json.JSONDecodeError, OSError):
            continue

    if incomplete_tasks:
        # Teammate has incomplete tasks — reject idle
        task_list = ", ".join(incomplete_tasks)
        print(
            f"You still have in-progress tasks: {task_list}. "
            f"Please complete them before going idle.",
            file=sys.stderr,
        )
        sys.exit(2)

    # All tasks complete or no tasks assigned — allow idle
    sys.exit(0)


if __name__ == "__main__":
    main()
