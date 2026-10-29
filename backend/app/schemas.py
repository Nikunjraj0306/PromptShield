from pydantic import BaseModel, Field


class InspectRequest(BaseModel):
    application_id: int = Field(gt=0)
    endpoint_id: int | None = Field(default=None, gt=0)
    text: str = Field(min_length=1, max_length=10_000)


class FindingResponse(BaseModel):
    rule_name: str
    category: str
    severity: str
    weight: int
    is_critical: bool
    evidence_summary: str


class InspectResponse(BaseModel):
    correlation_id: str
    risk_score: int
    decision: str
    reason_code: str
    findings: list[FindingResponse]
