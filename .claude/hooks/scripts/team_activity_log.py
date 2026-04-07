#!/usr/bin/env python3
"""PostToolUse hook for TeamCreate, TaskCreate, and TaskUpdate.

Logs team orchestration events to specs/team_activity.log for auditability.
Advisory only — always exits 0.

Hook context (stdin JSON):
  - tool_name: The tool that was called
  - tool_input: The input parameters
  - tool_output: The output from the tool (if PostToolUse)
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Only log team-related tools
    if tool_name not in ("TeamCreate", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet"):
        return

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build log entry
    if tool_name == "TeamCreate":
        team_name = tool_input.get("team_name", "unknown")
        entry = f"[{timestamp}] TEAM_CREATED: {team_name}"
    elif tool_name == "TaskCreate":
        subject = tool_input.get("subject", "unknown")
        entry = f"[{timestamp}] TASK_CREATED: {subject}"
    elif tool_name == "TaskUpdate":
        task_id = tool_input.get("taskId", "unknown")
        status = tool_input.get("status", "")
        owner = tool_input.get("owner", "")
        parts = [f"[{timestamp}] TASK_UPDATED: id={task_id}"]
        if status:
            parts.append(f"status={status}")
        if owner:
            parts.append(f"owner={owner}")
        entry = " ".join(parts)
    else:
        entry = f"[{timestamp}] {tool_name}: {json.dumps(tool_input)[:200]}"

    # Write to log file
    log_path = Path("specs/team_activity.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a") as f:
        f.write(entry + "\n")

    # Advisory only — never block
    sys.exit(0)


if __name__ == "__main__":
    main()
