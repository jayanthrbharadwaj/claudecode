#!/usr/bin/env python3
"""Block subagents from reading plugin cache files.

PreToolUse hook for Read operations.
- Subagents (transcript in /subagents/): exit 2 -> blocks the tool call
- Main conversation: exit 0 -> allows the read

In plugin context, blocks reads of the plugin cache directory
(detected from this script's own path) rather than .claude/.
"""
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPT_DIR.parent.parent


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return

    file_path = data.get("tool_input", {}).get("file_path", "")

    # Block reads of the plugin directory and .claude/ scaffold files
    plugin_path = str(PLUGIN_ROOT)
    is_plugin_file = file_path.startswith(plugin_path)
    is_scaffold_file = ".claude/" in file_path

    if not is_plugin_file and not is_scaffold_file:
        return  # Not a scaffold/plugin file, allow

    transcript = data.get("transcript_path", "")
    is_subagent = "/subagents/" in transcript

    if is_subagent:
        print(
            f"BLOCKED: '{file_path}' is scaffold/plugin infrastructure. "
            "Scaffold info is in CLAUDE.md. Skip all plugin and .claude/ files.",
            file=sys.stderr,
        )
        sys.exit(2)

    # Main conversation -- allow


if __name__ == "__main__":
    main()
