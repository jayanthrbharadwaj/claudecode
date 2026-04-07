#!/usr/bin/env python3
"""Secrets and PII output guard — hard-blocks credentials/PII in tool output.

PostToolUse hook for Bash/Write/Edit/MultiEdit.
Exit 2 = hard-block (cannot be bypassed by the agent).
"""
import json
import re
import sys
from pathlib import Path

# Compiled regex patterns for secrets detection
SECRET_PATTERNS = [
    # AWS access keys
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS Access Key"),
    # GitHub PATs
    (re.compile(r"ghp_[A-Za-z0-9]{36,}"), "GitHub Personal Access Token"),
    # GitHub OAuth tokens
    (re.compile(r"gho_[A-Za-z0-9]{36,}"), "GitHub OAuth Token"),
    # OpenAI keys
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "OpenAI/API Secret Key"),
    # Generic Bearer tokens
    (re.compile(r"Bearer\s+[A-Za-z0-9\-_.]{20,}"), "Bearer Token"),
    # Private key headers
    (re.compile(r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----"), "Private Key"),
    # Generic key/secret/password/token assignments
    (
        re.compile(
            r"""(?:api[_-]?key|api[_-]?secret|password|passwd|secret[_-]?key|access[_-]?token|auth[_-]?token)"""
            r"""\s*[=:]\s*["'][A-Za-z0-9+/=\-_.]{8,}["']""",
            re.IGNORECASE,
        ),
        "Hardcoded credential assignment",
    ),
    # Slack tokens
    (re.compile(r"xox[bpors]-[A-Za-z0-9\-]{10,}"), "Slack Token"),
    # Anthropic keys
    (re.compile(r"sk-ant-[A-Za-z0-9\-]{20,}"), "Anthropic API Key"),
    # Azure Storage account keys (base64, 88 chars with == padding)
    (re.compile(r"[A-Za-z0-9+/]{86}=="), "Azure Storage Account Key"),
    # Azure connection strings
    (
        re.compile(
            r"DefaultEndpointsProtocol=https?;AccountName=[^;]+;AccountKey=[A-Za-z0-9+/=]+",
        ),
        "Azure Storage Connection String",
    ),
    # Azure SAS tokens
    (
        re.compile(
            r"[?&]sig=[A-Za-z0-9%+/=]{20,}",
        ),
        "Azure SAS Token",
    ),
    # Azure SQL / Service Bus / Event Hub connection strings
    (
        re.compile(
            r"(?:Server|Endpoint)=sb?://[^;]+;SharedAccessKey=[A-Za-z0-9+/=]+",
            re.IGNORECASE,
        ),
        "Azure Service Connection String",
    ),
]

# PII patterns
PII_PATTERNS = [
    # SSN (XXX-XX-XXXX)
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "Social Security Number"),
    # Credit card numbers (basic Luhn-eligible patterns)
    (re.compile(r"\b(?:4\d{3}|5[1-5]\d{2}|3[47]\d{2}|6011)\d{12,15}\b"), "Credit Card Number"),
    (re.compile(r"\b\d{4}[- ]\d{4}[- ]\d{4}[- ]\d{4}\b"), "Credit Card Number (formatted)"),
]

# False positive exclusions: file patterns
EXCLUDED_FILE_PATTERNS = [
    ".env.example",
]

# False positive exclusions: line-level prefixes indicating test/dummy values
DUMMY_PREFIXES = [
    "test-",
    "fake-",
    "dummy-",
    "example-",
    "placeholder",
    "change-me",
    "xxx",
    "CHANGE_ME",
    "your-",
]


def is_excluded_file(file_path: str) -> bool:
    """Check if the file is in the exclusion list."""
    name = Path(file_path).name
    return name in EXCLUDED_FILE_PATTERNS


def is_test_file(file_path: str) -> bool:
    """Check if file is in a test directory or is a test file."""
    path = Path(file_path)
    parts = path.parts
    return "tests" in parts or "test" in parts or path.name.startswith("test_")


def is_regex_definition(line: str) -> bool:
    """Check if the line is defining a regex pattern (not an actual secret)."""
    indicators = ["re.compile", "Pattern", "regex", "PATTERN", "r\"", "r'"]
    return any(ind in line for ind in indicators)


def has_dummy_value(matched_text: str) -> bool:
    """Check if the matched text contains a known dummy/test prefix."""
    lower = matched_text.lower()
    return any(prefix in lower for prefix in DUMMY_PREFIXES)


def scan_content(content: str, file_path: str) -> list[dict[str, str]]:
    """Scan content for secrets and PII. Returns list of findings."""
    if is_excluded_file(file_path):
        return []

    findings: list[dict[str, str]] = []
    lines = content.split("\n")

    for line_num, line in enumerate(lines, 1):
        # Skip regex pattern definitions
        if is_regex_definition(line):
            continue

        # Check secret patterns
        for pattern, label in SECRET_PATTERNS:
            match = pattern.search(line)
            if match and not has_dummy_value(match.group()):
                # In test files, be more lenient
                if is_test_file(file_path) and has_dummy_value(line):
                    continue
                findings.append({
                    "type": "SECRET",
                    "label": label,
                    "line": line_num,
                    "file": file_path,
                })

        # Check PII patterns
        for pattern, label in PII_PATTERNS:
            match = pattern.search(line)
            if match and not has_dummy_value(match.group()):
                findings.append({
                    "type": "PII",
                    "label": label,
                    "line": line_num,
                    "file": file_path,
                })

    return findings


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    tool_output = data.get("tool_output", "")

    # Determine what content to scan
    content_to_scan = ""
    file_path = ""

    if tool_name in ("Write", "Edit", "MultiEdit"):
        file_path = tool_input.get("file_path", "")
        # Scan the content being written
        content_to_scan = tool_input.get("content", "")
        if not content_to_scan:
            content_to_scan = tool_input.get("new_string", "")
    elif tool_name == "Bash":
        file_path = "(bash output)"
        content_to_scan = str(tool_output)

    if not content_to_scan:
        sys.exit(0)

    findings = scan_content(content_to_scan, file_path)

    if findings:
        summary = "; ".join(
            f"{f['label']} ({f['type']}) at line {f['line']}"
            for f in findings[:5]
        )
        reason = f"Blocked: detected {len(findings)} secret/PII occurrence(s): {summary}"
        print(json.dumps({"decision": "block", "reason": reason}))
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
