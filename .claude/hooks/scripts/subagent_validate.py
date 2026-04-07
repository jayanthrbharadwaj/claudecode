#!/usr/bin/env python3
"""Subagent output validation hook.

PostToolUse hook for Task tool. Checks that subagent output includes
expected patterns based on agent type.
Advisory only (always exit 0).
"""
import json
import re
import sys


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return

    tool_result = data.get("tool_result", "")
    if isinstance(tool_result, dict):
        tool_result = json.dumps(tool_result)

    tool_input = data.get("tool_input", {})
    prompt = tool_input.get("prompt", "")
    if isinstance(prompt, dict):
        prompt = json.dumps(prompt)

    # Detect agent type from the prompt
    prompt_lower = prompt.lower()
    result_lower = tool_result.lower()

    # Check implementer output
    if "implementer" in prompt_lower or "implement" in prompt_lower:
        has_test_mention = any(
            keyword in result_lower
            for keyword in [
                "test", "passed", "failed", "coverage",
                "pytest", "jest", "make test",
            ]
        )
        if not has_test_mention:
            print(
                "subagent-validate: Implementer output does not mention "
                "test results. Verify tests were run."
            )

    # Check reviewer output
    reviewer_keywords = [
        "reviewer", "review", "spec-review",
        "code-review", "security-review",
    ]
    if any(kw in prompt_lower for kw in reviewer_keywords):
        verdict_patterns = [
            r"APPROVE",
            r"REQUEST_CHANGES",
            r"SPEC_COMPLIANT",
            r"SPEC_VIOLATIONS_FOUND",
        ]
        has_verdict = any(
            re.search(pattern, tool_result) for pattern in verdict_patterns
        )
        if not has_verdict:
            print(
                "subagent-validate: Reviewer output missing verdict. "
                "Expected one of: APPROVE, REQUEST_CHANGES, "
                "SPEC_COMPLIANT, SPEC_VIOLATIONS_FOUND."
            )


if __name__ == "__main__":
    main()
    sys.exit(0)
