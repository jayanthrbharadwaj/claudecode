#!/usr/bin/env python3
"""Commit alignment hook -- check commit messages reference stories.

PostToolUse hook for Bash. Only activates on git commit commands.
Advisory only (always exit 0).
"""
import json
import re
import subprocess
import sys
from pathlib import Path


def get_project_root() -> Path:
    """Detect project root via git."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return Path(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return Path(".")


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return

    # Check if this is a git commit command
    command = data.get("tool_input", {}).get("command", "")
    if not command:
        return

    # Only process git commit commands
    if "git commit" not in command:
        return

    # Extract commit message from -m flag
    msg_match = re.search(r'-m\s+["\'](.+?)["\']', command)
    if not msg_match:
        # Try heredoc or other patterns
        msg_match = re.search(r"-m\s+(\S+)", command)
    if not msg_match:
        return

    commit_msg = msg_match.group(1)

    # Check for story reference (US-XXX pattern)
    has_story_ref = bool(re.search(r"US-\d+", commit_msg, re.IGNORECASE))

    if has_story_ref:
        return  # All good

    # Check if there are story files
    project_root = get_project_root()
    stories_dir = project_root / "specs" / "stories"

    if stories_dir.is_dir() and any(stories_dir.glob("*.md")):
        print(
            "commit-alignment: Commit message has no story reference "
            "(US-XXX). Consider linking commits to user stories."
        )


if __name__ == "__main__":
    main()
    sys.exit(0)
