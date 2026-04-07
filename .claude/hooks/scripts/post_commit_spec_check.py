#!/usr/bin/env python3
"""Session-end spec coverage summary.

Stop hook. Informational only (always exit 0).
"""
import subprocess
import sys
from pathlib import Path


def git_changed_files() -> list[str]:
    files: set[str] = set()
    for cmd in (
        ["git", "diff", "--name-only", "HEAD"],
        ["git", "diff", "--cached", "--name-only"],
    ):
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.strip().splitlines():
                if line.strip():
                    files.add(line.strip())
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    return sorted(files)


def main() -> None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        project_root = (
            Path(result.stdout.strip()) if result.returncode == 0 else Path(".")
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        project_root = Path(".")

    changed = git_changed_files()
    if not changed:
        return

    total = len(changed)
    src_files = 0
    specs_found = 0
    specs_missing = 0
    specs_dir = project_root / "specs" / "features"

    for file in changed:
        if not file.startswith("src/"):
            continue
        src_files += 1
        basename = Path(file).stem
        if basename == "__init__":
            continue

        normalized = basename.replace("_", "-")
        if specs_dir.is_dir():
            existing = [
                p.stem.replace("_", "-") for p in specs_dir.glob("*.md")
            ]
            if normalized in existing:
                specs_found += 1
            else:
                specs_missing += 1
        else:
            specs_missing += 1

    print("=========================================")
    print("  Session Changes Summary")
    print("=========================================")
    print(f"  Files modified:   {total}")
    print(f"  Source files:      {src_files}")
    print(f"  Specs found:      {specs_found}")
    print(f"  Specs missing:    {specs_missing}")
    print("=========================================")


if __name__ == "__main__":
    main()
    sys.exit(0)
