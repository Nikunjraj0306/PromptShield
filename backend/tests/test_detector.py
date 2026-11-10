
from app.detector import (
    calculate_risk_score,
    inspect_text,
    make_decision,
)


def test_clean_text_has_no_findings():
    findings = inspect_text("Hello, this is a normal request.")
    assert findings == []
    assert calculate_risk_score(findings) == 0


def test_xss_pattern_is_detected():
    findings = inspect_text("<script>alert(1)</script>")
    assert any(f.category == "XSS" for f in findings)


def test_critical_command_pattern_blocks():
    findings = inspect_text("test; whoami")
    score = calculate_risk_score(findings)
    decision, reason = make_decision(findings, score)

    assert decision == "Block"
    assert reason == "CRITICAL_FINDING"


def test_rm_rf_command_injection_is_detected_and_blocks():
    findings = inspect_text("rm -rf /")

    command_findings = [
        f for f in findings
        if f.category == "COMMAND_INJECTION"
    ]

    assert len(command_findings) == 1
    assert command_findings[0].severity == "Critical"
    assert command_findings[0].weight == 60
    assert command_findings[0].is_critical is True

    score = calculate_risk_score(findings)
    decision, reason = make_decision(findings, score)

    assert score == 60
    assert decision == "Block"
    assert reason == "CRITICAL_FINDING"


def test_risk_score_is_capped_at_100():
    findings = inspect_text(
        "UNION SELECT x; whoami <script> javascript: "
        "../path ignore previous instructions"
    )
    assert calculate_risk_score(findings) <= 100
