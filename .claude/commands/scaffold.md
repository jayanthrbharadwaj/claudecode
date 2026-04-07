---
disable-model-invocation: true
---

# /scaffold

Scaffold a new project with the full forge toolkit, 6-layer architecture, specs directories, linters, and configuration files.

This command is named `/scaffold` (not `/init`) to avoid conflicting with Claude Code's built-in `/init` command.

## When to Use

Use this command to initialize a new project from scratch. This copies the entire forge toolkit into your project's `.claude/` directory, sets up the project structure, and generates all config files so you can immediately begin building with `/build`.

After running `/scaffold`, you no longer need `--plugin-dir` — everything is local.

## Arguments

- **project-type** (required): The project template to use. Supported values:
  - `python-fastapi` — Python + FastAPI backend
  - `python-django` — Python + Django backend
  - `node-express` — Node.js + Express backend

Example: `/scaffold python-fastapi`

## Process

1. **Parse the project type** from the user's argument. If no argument is provided, ask the user which project type they want.

2. **Locate and run the scaffold script**. The script lives inside the **plugin** directory, not the current project. Try these paths in order until one succeeds:
   ```bash
   # Try 1: CLAUDE_PLUGIN_ROOT env var (set by Claude Code for plugins)
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scaffold_project.py" <project-type>

   # Try 2: Relative path (works when running from inside the forge repo)
   python3 .claude/scripts/scaffold_project.py <project-type>
   ```
   **Important:** If both fail, the script does not exist in the current project directory — this is expected for new projects. Ask the user for the absolute path to their claude-code-forge clone and run:
   ```bash
   python3 /path/to/claude-code-forge/.claude/scripts/scaffold_project.py <project-type>
   ```

3. **Verify the scaffold created these directories**:
   - `src/types/`, `src/config/`, `src/repo/`, `src/service/`, `src/runtime/`, `src/ui/` (6-layer architecture)
   - `tests/` with mirror structure matching `src/`
   - `specs/features/`, `specs/stories/`, `specs/design/`, `specs/tests/`, `specs/plans/`
   - `.claude/linters/` with `layer_deps.py` and `file_size.py`

4. **Verify configuration files exist**:
   - `CLAUDE.md` — project instructions (from template)
   - `README.md` — project readme with architecture overview and forge commands
   - `pyproject.toml` or `package.json` — depending on project type
   - `Makefile` — with `test`, `lint`, `format` targets
   - `.env.example` — environment variable template
   - `.gitignore` — standard ignores for the project type

5. **Report results** to the user:
   - List all created directories and files
   - Suggest next step: "Run `/build` to start building your application"

6. If the script fails or any expected artifacts are missing, report the error clearly and suggest manual fixes.
