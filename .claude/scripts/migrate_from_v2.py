#!/usr/bin/env python3
"""Migration script for existing scaffold-v2 users.

Detects existing .claude/ scaffold structure and migrates to
plugin-based architecture. Preserves specs/ and linters/.

Usage: python3 migrate_from_v2.py [project-root]
"""
import json
import shutil
import sys
from pathlib import Path


def confirm(prompt: str) -> bool:
    """Ask user for confirmation."""
    response = input(f"{prompt} [y/N] ").strip().lower()
    return response in ("y", "yes")


def remove_directory(path: Path, label: str) -> bool:
    """Remove a directory with reporting."""
    if not path.is_dir():
        print(f"  skip (not found): {label}")
        return False
    file_count = sum(1 for _ in path.rglob("*") if _.is_file())
    print(f"  removing: {label} ({file_count} files)")
    shutil.rmtree(path)
    return True


def update_settings_json(claude_dir: Path) -> bool:
    """Remove hook registrations from settings.json."""
    settings_file = claude_dir / "settings.json"
    if not settings_file.exists():
        print("  skip (not found): .claude/settings.json")
        return False

    try:
        content = json.loads(settings_file.read_text())
    except (json.JSONDecodeError, OSError):
        print("  skip (invalid): .claude/settings.json")
        return False

    changed = False

    # Remove hooks section
    if "hooks" in content:
        del content["hooks"]
        changed = True
        print("  updated: removed hooks from .claude/settings.json")

    if changed:
        settings_file.write_text(
            json.dumps(content, indent=2) + "\n"
        )

    return changed


def main() -> None:
    project_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    project_root = project_root.resolve()
    claude_dir = project_root / ".claude"

    print(f"Migrating project at {project_root}")
    print()

    if not claude_dir.is_dir():
        print("No .claude/ directory found. Nothing to migrate.")
        sys.exit(0)

    # Detection phase
    print("Detected scaffold-v2 components:")
    agents_dir = claude_dir / "agents"
    hooks_dir = claude_dir / "hooks"
    templates_dir = claude_dir / "templates"
    linters_dir = claude_dir / "linters"
    specs_dir = project_root / "specs"

    components = {
        "agents": agents_dir.is_dir(),
        "hooks": hooks_dir.is_dir(),
        "templates": templates_dir.is_dir(),
        "linters": linters_dir.is_dir(),
        "specs": specs_dir.is_dir(),
    }

    for name, exists in components.items():
        status = "found" if exists else "not found"
        print(f"  .claude/{name}: {status}")
    if components["specs"]:
        print(f"  specs/: found (will be preserved)")
    print()

    if not any(components.values()):
        print("No scaffold-v2 components found. Nothing to migrate.")
        sys.exit(0)

    if not confirm("Proceed with migration?"):
        print("Migration cancelled.")
        sys.exit(0)

    print()
    print("Migration steps:")

    removed = 0
    kept = 0

    # Remove agents (now in plugin)
    if remove_directory(agents_dir, ".claude/agents/"):
        removed += 1

    # Remove hooks (now in plugin)
    if remove_directory(hooks_dir, ".claude/hooks/"):
        removed += 1

    # Remove templates (now in plugin)
    if remove_directory(templates_dir, ".claude/templates/"):
        removed += 1

    # Keep linters (needed for CI)
    if linters_dir.is_dir():
        print("  keeping: .claude/linters/ (needed for CI)")
        kept += 1

    # Keep specs
    if specs_dir.is_dir():
        print("  keeping: specs/ (project data)")
        kept += 1

    # Update settings.json
    update_settings_json(claude_dir)

    # Remove docs if present (now in plugin)
    docs_dir = claude_dir / "docs"
    if remove_directory(docs_dir, ".claude/docs/"):
        removed += 1

    # Remove scripts if present (now in plugin)
    scripts_dir = claude_dir / "scripts"
    if remove_directory(scripts_dir, ".claude/scripts/"):
        removed += 1

    # Remove evals if present (now in plugin)
    evals_dir = claude_dir / "evals"
    if remove_directory(evals_dir, ".claude/evals/"):
        removed += 1

    print()
    print("=========================================")
    print("  Migration Summary")
    print("=========================================")
    print(f"  Directories removed:  {removed}")
    print(f"  Directories kept:     {kept}")
    print("  settings.json:        updated")
    print()
    print("  Next steps:")
    print("  1. Install claude-code-forge plugin")
    print("  2. Run /forge:validate to verify setup")
    print("  3. Commit the changes")
    print("=========================================")


if __name__ == "__main__":
    main()
