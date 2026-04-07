#!/usr/bin/env python3
"""Plugin integrity checker.

Validates that all expected plugin files exist and are well-formed.

Usage: python3 validate_plugin.py [plugin-root]
"""
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_PLUGIN_ROOT = SCRIPT_DIR.parent.parent

EXPECTED_AGENTS = [
    "spec-writer.md",
    "implementer.md",
    "test-writer.md",
    "e2e-writer.md",
    "devops.md",
    "spec-reviewer.md",
    "code-reviewer.md",
    "security-reviewer.md",
    "pr-writer.md",
    "refactorer.md",
    "research-agent.md",
    "debug-agent.md",
    "pipeline-orchestrator.md",
    "performance-reviewer.md",
    "design-consistency-checker.md",
    "code-simplifier.md",
    "housekeeper.md",
    "architecture-alignment-checker.md",
    "prd-architecture-checker.md",
    "task-executor.md",
]

EXPECTED_COMMANDS = [
    "init.md",
    "build.md",
    "add-feature.md",
    "resume.md",
    "design.md",
    "work-on-next.md",
    "validate.md",
    "review.md",
    "debug.md",
    "create-pr.md",
    "refactor.md",
    "spec-sync.md",
    "just-do-it.md",
    "build-unplanned.md",
    "design-architecture.md",
    "design-product.md",
    "create-tasks.md",
    "work-on.md",
    "source-architecture.md",
    "source-specs.md",
    "skills.md",
    "check.md",
    "help.md",
]

EXPECTED_SKILLS = [
    "routing",
    "sdlc-pipeline",
    "layer-enforcement",
    "conventions",
    "spec-sync-engine",
    "worktree-isolation",
    "verification-suite",
    "teams",
    "test-driven-development",
    "validation-loop",
    "task-validation-loop",
    "implement-feature",
    "execute-task",
    "next-task",
    "tasks",
    "build-unplanned-feature",
    "understanding-feature-requests",
    "architecture",
    "design-system",
    "check-alignment",
    "sync-architecture",
    "sync-design-system",
    "debugging",
]

EXPECTED_HOOK_SCRIPTS = [
    "pre_write_check.py",
    "post_write_lint.py",
    "pre_read_scaffold_guard.py",
    "post_commit_spec_check.py",
    "session_start.py",
    "pre_compact_save.py",
    "commit_alignment.py",
    "subagent_validate.py",
    "team_activity_log.py",
    "teammate_idle_check.py",
    "task_completed_check.py",
]

EXPECTED_LINTERS = [
    "layer_deps.py",
    "file_size.py",
    "lint_all.py",
]

EXPECTED_TEMPLATES = [
    "app_spec.md",
    "feature_spec.md",
    "feature_spec_lite.md",
    "user_stories.md",
    "design_doc.md",
    "test_plan.md",
    "execution_plan.md",
    "pipeline_status.md",
]

EXPECTED_PROJECT_TEMPLATES = [
    "CLAUDE.md.j2",
    "pyproject.toml.j2",
    "Makefile.j2",
    "Dockerfile.j2",
    "ci.yml.j2",
]

EXPECTED_DOCS = [
    "architecture.md",
    "pipeline.md",
    "conventions.md",
    "testing-standard.md",
    "git-workflow.md",
]


def check_file(path: Path, label: str) -> bool:
    exists = path.is_file()
    status = "OK" if exists else "MISSING"
    print(f"  [{status}] {label}")
    return exists


def check_json(path: Path, label: str) -> bool:
    if not path.is_file():
        print(f"  [MISSING] {label}")
        return False
    try:
        json.loads(path.read_text())
        print(f"  [OK] {label}")
        return True
    except (json.JSONDecodeError, OSError) as e:
        print(f"  [INVALID] {label}: {e}")
        return False


def main() -> None:
    plugin_root = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1
        else DEFAULT_PLUGIN_ROOT
    )

    print(f"Validating plugin at {plugin_root}")
    print()

    total = 0
    passed = 0

    # 1. Plugin manifest
    print("Plugin manifest:")
    total += 1
    if check_json(plugin_root / ".claude" / ".claude-plugin" / "plugin.json", ".claude/.claude-plugin/plugin.json"):
        passed += 1
    print()

    # 2. Agents
    print(f"Agents ({len(EXPECTED_AGENTS)} expected):")
    for agent in EXPECTED_AGENTS:
        total += 1
        if check_file(plugin_root / ".claude" / "agents" / agent, f".claude/agents/{agent}"):
            passed += 1
    print()

    # 3. Commands
    print(f"Commands ({len(EXPECTED_COMMANDS)} expected):")
    for cmd in EXPECTED_COMMANDS:
        total += 1
        if check_file(plugin_root / ".claude" / "commands" / cmd, f".claude/commands/{cmd}"):
            passed += 1
    print()

    # 4. Skills
    print(f"Skills ({len(EXPECTED_SKILLS)} expected):")
    for skill in EXPECTED_SKILLS:
        total += 1
        if check_file(plugin_root / ".claude" / "skills" / skill / "SKILL.md", f".claude/skills/{skill}/SKILL.md"):
            passed += 1
    print()

    # 5. Hooks
    print("Hooks:")
    total += 1
    if check_json(plugin_root / ".claude" / "hooks" / "hooks.json", ".claude/hooks/hooks.json"):
        passed += 1
    print(f"Hook scripts ({len(EXPECTED_HOOK_SCRIPTS)} expected):")
    for script in EXPECTED_HOOK_SCRIPTS:
        total += 1
        if check_file(plugin_root / ".claude" / "hooks" / "scripts" / script, f".claude/hooks/scripts/{script}"):
            passed += 1
    print()

    # 6. Linters
    print(f"Linters ({len(EXPECTED_LINTERS)} expected):")
    for linter in EXPECTED_LINTERS:
        total += 1
        if check_file(plugin_root / ".claude" / "linters" / linter, f".claude/linters/{linter}"):
            passed += 1
    print()

    # 7. Templates
    print(f"Templates ({len(EXPECTED_TEMPLATES)} spec templates):")
    for tpl in EXPECTED_TEMPLATES:
        total += 1
        if check_file(plugin_root / ".claude" / "templates" / tpl, f".claude/templates/{tpl}"):
            passed += 1
    print()

    print(f"Project templates ({len(EXPECTED_PROJECT_TEMPLATES)} expected):")
    for tpl in EXPECTED_PROJECT_TEMPLATES:
        total += 1
        if check_file(plugin_root / ".claude" / "templates" / "project" / tpl, f".claude/templates/project/{tpl}"):
            passed += 1
    print()

    print("E2E templates:")
    total += 1
    e2e_path = plugin_root / ".claude" / "templates" / "e2e"
    if e2e_path.is_dir() and (e2e_path / "conftest.py").is_file():
        print(f"  [OK] .claude/templates/e2e/ (conftest.py present)")
        passed += 1
    else:
        print(f"  [MISSING] .claude/templates/e2e/")
    print()

    # 8. Docs
    print(f"Docs ({len(EXPECTED_DOCS)} expected):")
    for doc in EXPECTED_DOCS:
        total += 1
        if check_file(plugin_root / ".claude" / "docs" / doc, f".claude/docs/{doc}"):
            passed += 1
    print()

    # 9. Config files
    print("Config files:")
    for config in [".claude/settings.json", ".claude/.mcp.json", "README.md"]:
        total += 1
        if check_file(plugin_root / config, config):
            passed += 1
    print()

    # Summary
    failed = total - passed
    status = "PASS" if failed == 0 else "FAIL"
    print("=========================================")
    print(f"  Plugin Validation: {status}")
    print("=========================================")
    print(f"  Total checked:  {total}")
    print(f"  Passed:         {passed}")
    print(f"  Failed:         {failed}")
    print("=========================================")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
