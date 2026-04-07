#!/usr/bin/env python3
"""Forward-only layer dependency check.

Layer order: types=0, config=1, repo=2, service=3, runtime=4, ui=5
A file in layer N can only import from layers 0..N.
"""
import re
import sys
from pathlib import Path

LAYERS = ["types", "config", "repo", "service", "runtime", "ui"]
LAYER_INDEX = {name: i for i, name in enumerate(LAYERS)}


def get_layer(filepath: str) -> str | None:
    for layer in LAYERS:
        if f"src/{layer}/" in filepath:
            return layer
    return None


def get_import_layer(target: str) -> str | None:
    for layer in LAYERS:
        if re.search(rf"(^|\.)(src\.)?{layer}(\.|$)", target):
            return layer
    return None


def check_file(pyfile: Path) -> int:
    file_layer = get_layer(str(pyfile))
    if file_layer is None:
        return 0

    file_index = LAYER_INDEX[file_layer]
    errors = 0

    for line_num, line in enumerate(pyfile.read_text().splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        import_target = ""
        match_from = re.match(r"^from\s+([a-zA-Z0-9_.]+)\s+import", stripped)
        match_import = re.match(r"^import\s+([a-zA-Z0-9_.]+)", stripped)

        if match_from:
            import_target = match_from.group(1)
        elif match_import:
            import_target = match_import.group(1)

        if not import_target:
            continue

        import_layer = get_import_layer(import_target)
        if import_layer is None:
            continue

        import_index = LAYER_INDEX[import_layer]
        if import_index > file_index:
            print(
                f"LAYER_DEPS: {pyfile}:{line_num} layer"
                f" '{file_layer}' ({file_index}) imports"
                f" '{import_layer}' ({import_index})."
            )
            print(
                f"  Remediation: Layer '{file_layer}' cannot import"
                f" from '{import_layer}'. Move the dependency or refactor."
            )
            print(
                "  Order: types(0) -> config(1) -> repo(2)"
                " -> service(3) -> runtime(4) -> ui(5)"
            )
            print()
            errors += 1

    return errors


def main() -> None:
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "src/"
    target = Path(target_dir)

    errors = 0
    for pyfile in sorted(target.rglob("*.py")):
        errors += check_file(pyfile)

    if errors > 0:
        print(f"layer_deps: {errors} violation(s) found.")
        sys.exit(1)
    print("layer_deps: OK")


if __name__ == "__main__":
    main()
