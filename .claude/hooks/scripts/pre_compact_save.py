#!/usr/bin/env python3
"""Pre-compact context save -- preserve pipeline state across compaction.

Prints a CONTEXT SAVE block summarizing current pipeline state so the model
can reconstruct state after context compaction.
Always exits 0.
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


def main() -> None:
    project_root = get_project_root()
    status_file = project_root / "specs" / "pipeline_status.md"

    if not status_file.exists():
        print("CONTEXT SAVE: No active pipeline.")
        sys.exit(0)

    try:
        content = status_file.read_text()
    except OSError:
        print("CONTEXT SAVE: Could not read pipeline status.")
        sys.exit(0)

    # Extract phase statuses
    phases: list[str] = []
    for match in re.finditer(
        r"\|\s*(\w[\w\s]*?)\s*\|\s*(Done|In Progress|Pending|Skipped)\s*\|",
        content,
    ):
        phase_name = match.group(1).strip()
        phase_status = match.group(2).strip()
        if phase_name.lower() not in ("phase", "---"):
            phases.append(f"  {phase_name}: {phase_status}")

    # Extract feature name
    feature = "Unknown"
    match = re.search(r"##\s+Feature:\s*(.+)", content)
    if match:
        feature = match.group(1).strip()

    # Extract current phase
    current = "Unknown"
    match = re.search(r"Current Phase:\s*\*\*(.+?)\*\*", content)
    if not match:
        match = re.search(r"Current Phase:\s*(.+)", content)
    if match:
        current = match.group(1).strip()

    print("=== CONTEXT SAVE: Pipeline State ===")
    print(f"Feature: {feature}")
    print(f"Current Phase: {current}")
    if phases:
        print("Phase Status:")
        for p in phases:
            print(p)
    print("=== END CONTEXT SAVE ===")


if __name__ == "__main__":
    main()
    sys.exit(0)
