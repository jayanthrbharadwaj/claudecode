#!/usr/bin/env python3
"""Environment protection guard — tiered deployment approval.

PreToolUse hook for Bash commands.
Production/staging deploys are hard-blocked (exit 2).
Dev deploys are advisory only (exit 0 with warning).
"""
import json
import re
import sys

# Production patterns — hard-block (exit 2)
PRODUCTION_PATTERNS = [
    re.compile(r"docker\s+push\s+.*prod", re.IGNORECASE),
    re.compile(r"kubectl\s+apply\s+.*prod", re.IGNORECASE),
    re.compile(r"kubectl\s+delete\s+.*prod", re.IGNORECASE),
    re.compile(r"helm\s+(?:install|upgrade)\s+.*prod", re.IGNORECASE),
    re.compile(r"terraform\s+destroy", re.IGNORECASE),
    re.compile(r"terraform\s+apply\s+.*prod", re.IGNORECASE),
    re.compile(r"git\s+push\s+.*\b(?:main|master)\b"),
    re.compile(r"git\s+push\s+--force"),
    re.compile(r"git\s+push\s+-f\b"),
    # Destructive SQL against production
    re.compile(r"(?:DROP|TRUNCATE|DELETE\s+FROM)\s+", re.IGNORECASE),
    # AWS/Azure/GCP production deployments
    re.compile(r"aws\s+.*--profile\s+.*prod", re.IGNORECASE),
    re.compile(r"az\s+.*prod", re.IGNORECASE),
    re.compile(r"gcloud\s+.*prod", re.IGNORECASE),
]

# Staging patterns — hard-block with warning (exit 2)
STAGING_PATTERNS = [
    re.compile(r"docker\s+push\s+.*stag", re.IGNORECASE),
    re.compile(r"kubectl\s+apply\s+.*stag", re.IGNORECASE),
    re.compile(r"kubectl\s+delete\s+.*stag", re.IGNORECASE),
    re.compile(r"helm\s+(?:install|upgrade)\s+.*stag", re.IGNORECASE),
    re.compile(r"terraform\s+apply\s+.*stag", re.IGNORECASE),
    re.compile(r"aws\s+.*--profile\s+.*stag", re.IGNORECASE),
]

# Dev patterns — advisory only (exit 0)
DEV_PATTERNS = [
    re.compile(r"docker\s+push\s+.*dev", re.IGNORECASE),
    re.compile(r"kubectl\s+apply\s+.*dev", re.IGNORECASE),
    re.compile(r"terraform\s+apply\s+.*dev", re.IGNORECASE),
]


def check_command(command: str) -> tuple[str, str] | None:
    """Check command against tiered environment patterns.

    Returns (tier, matched_pattern) or None.
    """
    for pattern in PRODUCTION_PATTERNS:
        if pattern.search(command):
            return ("production", pattern.pattern)

    for pattern in STAGING_PATTERNS:
        if pattern.search(command):
            return ("staging", pattern.pattern)

    for pattern in DEV_PATTERNS:
        if pattern.search(command):
            return ("dev", pattern.pattern)

    return None


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")
    if not command:
        sys.exit(0)

    result = check_command(command)
    if result is None:
        sys.exit(0)

    tier, _pattern = result

    if tier == "production":
        reason = (
            "BLOCKED: Production deployment detected. "
            "Production deploys require human approval via Claude Code's hook override. "
            f"Command: {command[:100]}"
        )
        print(json.dumps({"decision": "block", "reason": reason}))
        sys.exit(2)

    if tier == "staging":
        reason = (
            "BLOCKED: Staging deployment detected. "
            "Staging deploys require human confirmation. "
            f"Command: {command[:100]}"
        )
        print(json.dumps({"decision": "block", "reason": reason}))
        sys.exit(2)

    if tier == "dev":
        # Advisory only — print warning but allow
        print(
            json.dumps({
                "decision": "allow",
                "reason": f"Advisory: Dev environment deployment detected: {command[:100]}",
            })
        )
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
