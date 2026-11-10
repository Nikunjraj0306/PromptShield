
import re
from dataclasses import dataclass


@dataclass
class Finding:
    rule_name: str
    category: str
    severity: str
    weight: int
    is_critical: bool
    confidence: float | None
    evidence_summary: str


# Starter heuristics for demonstration only.
# These patterns are not a substitute for secure application design.
RULES = [
    {
        "name": "SQL Injection Pattern",
        "category": "SQL_INJECTION",
        "severity": "High",
        "weight": 35,
        "is_critical": False,
        "pattern": re.compile(
            r"(\bUNION\s+SELECT\b|'\s*(OR|AND)\s+['0-9]+\s*=\s*['0-9]+|--\s*$)",
            re.IGNORECASE,
        ),
    },
    {
        "name": "Cross-Site Scripting Pattern",
        "category": "XSS",
        "severity": "High",
        "weight": 35,
        "is_critical": False,
        "pattern": re.compile(
            r"<\s*script\b|javascript\s*:|onerror\s*=",
            re.IGNORECASE,
        ),
    },
    {
        "name": "Path Traversal Pattern",
        "category": "PATH_TRAVERSAL",
        "severity": "High",
        "weight": 35,
        "is_critical": False,
        "pattern": re.compile(
            r"\.\.[/\\]|%2e%2e",
            re.IGNORECASE,
        ),
    },
    {
        "name": "Command Injection Pattern",
        "category": "COMMAND_INJECTION",
        "severity": "Critical",
        "weight": 60,
        "is_critical": True,
        "pattern": re.compile(
            r"(?:^|;|&&?|\|\|?|\n|`|\$\()\s*"
            r"(?:sudo\s+)?"
            r"(?:whoami|id|cat|type|dir|pwd|uname|curl|wget|"
            r"bash|sh|powershell|cmd|nc|netcat|python|python3|"
            r"perl|ruby|chmod|chown)\b"
            r"|(?:^|\s)rm\s+-(?:[a-z]*r[a-z]*f[a-z]*|"
            r"[a-z]*f[a-z]*r[a-z]*)\s+",
            re.IGNORECASE,
        ),
    },
    {
        "name": "Prompt Injection Pattern",
        "category": "PROMPT_INJECTION",
        "severity": "Medium",
        "weight": 25,
        "is_critical": False,
        "pattern": re.compile(
            r"ignore\s+(all\s+)?previous\s+instructions|"
            r"reveal\s+(the\s+)?system\s+prompt",
            re.IGNORECASE,
        ),
    },
    {
        "name": "Sensitive Data Pattern",
        "category": "SENSITIVE_DATA",
        "severity": "High",
        "weight": 35,
        "is_critical": False,
        "pattern": re.compile(
            r"\b\d{3}-\d{2}-\d{4}\b|"
            r"\b(?:\d[ -]?){13,19}\b"
        ),
    },
]


def inspect_text(text: str) -> list[Finding]:
    findings: list[Finding] = []

    for rule in RULES:
        if rule["pattern"].search(text):
            findings.append(
                Finding(
                    rule_name=rule["name"],
                    category=rule["category"],
                    severity=rule["severity"],
                    weight=rule["weight"],
                    is_critical=rule["is_critical"],
                    confidence=None,
                    evidence_summary=(
                        f"Matched heuristic rule: {rule['name']}"
                    ),
                )
            )

    return findings


def calculate_risk_score(findings: list[Finding]) -> int:
    return min(100, sum(max(0, finding.weight) for finding in findings))


def make_decision(
    findings: list[Finding],
    risk_score: int,
    threshold: int = 50,
) -> tuple[str, str]:
    if any(finding.is_critical for finding in findings):
        return "Block", "CRITICAL_FINDING"

    if risk_score >= threshold:
        return "Block", "RISK_THRESHOLD_EXCEEDED"

    return "Allow", "NO_BLOCKING_RULE_MATCHED"
