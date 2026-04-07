#!/usr/bin/env python3
"""Directory scope guard — hard-blocks file access outside project root.

PreToolUse hook for Read/Write/Edit/MultiEdit/Bash.
Exit 2 = hard-block (cannot be bypassed by the agent).
"""
import json
import subprocess
import sys
from pathlib import Path


# Blocked home-relative directories (credential stores, config)
BLOCKED_PREFIXES = [
    "~/.ssh/",
    "~/.gnupg/",
    "~/.aws/",
    "~/.config/",
    "~/.azure/",
    "~/.kube/",
    "~/",
]

# Blocked absolute prefixes
BLOCKED_ABS_PREFIXES = [
    "/etc/",
    "/var/",
]

# Blocked env files (but .env.example is allowed)
BLOCKED_ENV_FILES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.staging",
}

# Patterns to detect in Bash commands
BASH_BLOCKED_PATTERNS = [
    "~/.ssh/",
    "~/.gnupg/",
    "~/.aws/",
    "~/.config/",
    "~/.azure/",
    "~/.kube/",
    "/etc/passwd",
    "/etc/shadow",
    "/etc/hosts",
    "cat ~/.",
    "cat /etc/",
    "cat ~/.ssh/",
    "cat ~/.aws/",
    "ssh-add ",
    "gpg --export-secret",
]


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
            return Path(result.stdout.strip()).resolve()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return Path(".").resolve()


def is_within_project(file_path: str, project_root: Path) -> bool:
    """Check if resolved path is within the project root."""
    resolved = Path(file_path).resolve()
    try:
        resolved.relative_to(project_root)
        return True
    except ValueError:
        return False


def is_blocked_env_file(file_path: str) -> bool:
    """Check if path points to a blocked .env file."""
    name = Path(file_path).name
    return name in BLOCKED_ENV_FILES


def check_file_path(file_path: str, project_root: Path) -> str | None:
    """Return a block reason if file_path is outside scope, else None."""
    if not file_path:
        return None

    # Expand ~ for comparison
    expanded = str(Path(file_path).expanduser())

    # Check blocked home-relative prefixes
    for prefix in BLOCKED_PREFIXES:
        expanded_prefix = str(Path(prefix).expanduser())
        if expanded.startswith(expanded_prefix):
            return f"Access to {prefix} is blocked by security policy"

    # Check blocked absolute prefixes
    for prefix in BLOCKED_ABS_PREFIXES:
        if expanded.startswith(prefix):
            return f"Access to {prefix} is blocked by security policy"

    # Check blocked .env files (allow .env.example)
    if is_blocked_env_file(file_path):
        return f"Access to {Path(file_path).name} is blocked — use .env.example for templates"

    # Check project scope via resolve (defeats ../ traversal)
    if not is_within_project(file_path, project_root):
        return "File is outside project directory — all access must be within project root"

    return None


def check_bash_command(command: str) -> str | None:
    """Return a block reason if Bash command accesses blocked paths."""
    for pattern in BASH_BLOCKED_PATTERNS:
        if pattern in command:
            return f"Bash command references blocked path: {pattern}"
    return None


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    project_root = get_project_root()

    # For file-based tools: check file_path
    if tool_name in ("Read", "Write", "Edit", "MultiEdit"):
        file_path = tool_input.get("file_path") or tool_input.get("path") or ""
        reason = check_file_path(file_path, project_root)
        if reason:
            print(json.dumps({"decision": "block", "reason": reason}))
            sys.exit(2)

    # For Bash: scan command string
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        reason = check_bash_command(command)
        if reason:
            print(json.dumps({"decision": "block", "reason": reason}))
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
