
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class InspectRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    application_id: int = Field(gt=0)
    endpoint_id: int = Field(gt=0)
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


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class CurrentUserResponse(BaseModel):
    user_id: int
    email: str
    role: str
