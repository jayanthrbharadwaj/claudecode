#!/usr/bin/env python3
"""File size linter — max 300 lines/file (warn 250), max 50 lines/function."""
import re
import sys
from pathlib import Path

CODE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx"}


def check_file_sizes(target: Path) -> int:
    errors = 0
    for f in sorted(target.rglob("*")):
        if f.suffix not in CODE_EXTENSIONS or not f.is_file():
            continue
        lines = f.read_text().splitlines()
        count = len(lines)
        if count > 300:
            print(
                f"FILE_SIZE: {f} has {count} lines (max 300)."
                " Split into smaller modules."
            )
            print(
                "  Remediation: Extract cohesive groups of"
                " functions into separate files."
            )
            print()
            errors += 1
        elif count > 250:
            print(
                f"FILE_SIZE_WARN: {f} has {count} lines"
                " (approaching 300 limit). Consider splitting."
            )
    return errors


def check_function_sizes(target: Path) -> int:
    errors = 0
    func_pattern = re.compile(r"^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\(")

    for f in sorted(target.rglob("*.py")):
        if not f.is_file():
            continue
        lines = f.read_text().splitlines()
        func_name = ""
        func_start = 0

        for line_num, line in enumerate(lines, start=1):
            match = func_pattern.match(line)
            if match:
                # Close previous function
                if func_name:
                    func_len = line_num - func_start
                    if func_len > 50:
                        print(
                            f"FUNC_SIZE: {f}:{func_start} function"
                            f" '{func_name}' has {func_len} lines"
                            " (max 50). Extract helpers."
                        )
                        print(
                            "  Remediation: Break into smaller"
                            " functions with clear, descriptive names."
                        )
                        print()
                        errors += 1
                func_name = match.group(1)
                func_start = line_num

        # Check last function
        if func_name:
            func_len = len(lines) - func_start + 1
            if func_len > 50:
                print(
                    f"FUNC_SIZE: {f}:{func_start} function"
                    f" '{func_name}' has {func_len} lines"
                    " (max 50). Extract helpers."
                )
                print(
                    "  Remediation: Break into smaller"
                    " functions with clear, descriptive names."
                )
                print()
                errors += 1

    return errors


def main() -> None:
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "src/"
    target = Path(target_dir)

    errors = check_file_sizes(target) + check_function_sizes(target)

    if errors > 0:
        print(f"file_size: {errors} violation(s) found.")
        sys.exit(1)
    print("file_size: OK")


if __name__ == "__main__":
    main()
