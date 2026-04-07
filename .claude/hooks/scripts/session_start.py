#!/usr/bin/env python3
"""Session start hook -- print pipeline status summary.

Called from the routing skill on first load.
Always exits 0 (advisory).
"""
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


def parse_pipeline_status(content: str) -> dict[str, str]:
    """Extract key fields from pipeline_status.md."""
    info: dict[str, str] = {}

    # Feature name
    match = re.search(r"##\s+Feature:\s*(.+)", content)
    if match:
        info["feature"] = match.group(1).strip()

    # Current phase
    match = re.search(r"Current Phase:\s*\*\*(.+?)\*\*", content)
    if not match:
        match = re.search(r"Current Phase:\s*(.+)", content)
    if match:
        info["phase"] = match.group(1).strip()

    # Last update
    match = re.search(r"Last Updated?:\s*(.+)", content)
    if match:
        info["last_update"] = match.group(1).strip()

    return info


def main() -> None:
    project_root = get_project_root()
    status_file = project_root / "specs" / "pipeline_status.md"

    if not status_file.exists():
        print(
            "No active pipeline. "
            "Use /forge:build or /forge:add-feature to start."
        )
        sys.exit(0)

    try:
        content = status_file.read_text()
    except OSError:
        print("Could not read pipeline status file.")
        sys.exit(0)

    info = parse_pipeline_status(content)

    print("=========================================")
    print("  Pipeline Status")
    print("=========================================")
    if info.get("feature"):
        print(f"  Feature:      {info['feature']}")
    if info.get("phase"):
        print(f"  Phase:        {info['phase']}")
    if info.get("last_update"):
        print(f"  Last update:  {info['last_update']}")
    print("=========================================")


if __name__ == "__main__":
    main()
    sys.exit(0)
