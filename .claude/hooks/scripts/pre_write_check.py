#!/usr/bin/env python3
"""Pre-write advisory hook -- quality reminders, never blocks.

PreToolUse hook for Write/Edit operations.
Reads tool input JSON from stdin, prints reminders, always exits 0.
"""
import json
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

    file_path = (
        data.get("tool_input", {}).get("file_path")
        or data.get("tool_input", {}).get("path")
        or ""
    )
    if not file_path:
        return

    is_src = "/src/" in file_path or file_path.startswith("src/")
    is_tests = "/tests/" in file_path or file_path.startswith("tests/")

    if not is_src and not is_tests:
        return

    # Layer reminder for src/ writes
    if is_src:
        layers = ["types", "config", "repo", "service", "runtime", "ui"]
        for layer in layers:
            if f"src/{layer}/" in file_path:
                print(
                    f"pre-write-check: Writing to '{layer}' layer."
                    " Imports only from lower layers."
                )
                break

        # Spec suggestion for new service modules
        name = Path(file_path).stem
        if "src/service/" in file_path and name not in ("__init__", "conftest"):
            project_root = get_project_root()
            feature_id = name.replace("_", "-")
            spec_path = project_root / "specs" / "features" / f"{feature_id}.md"
            if not spec_path.exists():
                print(
                    f"pre-write-check: No spec found for '{feature_id}'."
                    " Consider creating one with /forge:build."
                )

    print("pre-write-check: Remember to add/update tests for this change.")


if __name__ == "__main__":
    main()
