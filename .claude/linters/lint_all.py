#!/usr/bin/env python3
"""Master runner for custom linters."""
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LINTER_DIR = SCRIPT_DIR

LINTERS = ["layer_deps", "file_size"]


def main() -> None:
    passed = 0
    failed = 0
    results: list[str] = []

    print("=== Custom Linter Suite ===")
    print()

    for linter in LINTERS:
        script = LINTER_DIR / f"{linter}.py"
        if not script.exists():
            print(f"SKIP: {linter} (not found)")
            results.append(f"SKIP  {linter}")
            continue

        print(f"--- Running: {linter} ---")
        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True,
                text=True,
                timeout=60,
            )
        except subprocess.TimeoutExpired:
            print(f"  {linter}: TIMEOUT")
            results.append(f"FAIL  {linter}")
            failed += 1
            print()
            continue

        if result.returncode == 0:
            print(f"  {linter}: PASS")
            passed += 1
            results.append(f"PASS  {linter}")
        else:
            print(result.stdout, end="")
            print(f"  {linter}: FAIL")
            failed += 1
            results.append(f"FAIL  {linter}")
        print()

    print("=== Summary ===")
    print()
    for r in results:
        print(f"  {r}")
    print()
    print(f"  Passed: {passed} / {passed + failed}")

    if failed > 0:
        print(f"  FAILED: {failed} linter(s) reported issues.")
        sys.exit(1)
    print("  All linters passed.")


if __name__ == "__main__":
    main()
