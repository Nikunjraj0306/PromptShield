
import logging

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.middleware.cors import CORSMiddleware



from app.analytics_service import get_security_summary
from app.auth_dependencies import get_current_user, require_roles
from app.auth_service import authenticate_user, get_user_profile
from app.config import settings
from app.database import check_database_connection
from app.events_service import get_recent_events
from app.inspection_service import inspect_and_store
from app.rate_limiter import login_limiter
from app.schemas import (
    CurrentUserResponse,
    InspectRequest,
    InspectResponse,
    LoginRequest,
    TokenResponse,
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="PromptShield application security gateway API",
)

origins = [
    origin.strip()
    for origin in settings.cors_origins.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Correlation-ID"],
)


# --------------------------------------------------
# HEALTH CHECKS
# --------------------------------------------------

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "PromptShield API",
    }


@app.get("/health/ready", tags=["Health"])
def readiness_check():
    try:
        if not check_database_connection():
            raise HTTPException(
                status_code=503,
                detail="Database is not ready",
            )

        return {
            "status": "ready",
            "database": "connected",
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Database readiness check failed")

        raise HTTPException(
            status_code=503,
            detail="Database is unavailable",
        ) from None


# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------


@app.post(
    "/api/v1/auth/login",
    response_model=TokenResponse,
    tags=["Authentication"],
)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    client_ip = request.client.host if request.client else "unknown"
    limiter_key = f"{client_ip}|{form_data.username.strip().lower()}"

    wait_seconds = login_limiter.is_blocked(limiter_key)
    if wait_seconds > 0:
        raise HTTPException(
            status_code=429,
            detail="Too many failed login attempts. Please try again later.",
            headers={"Retry-After": str(wait_seconds)},
        )

    try:
        result = authenticate_user(
            email=form_data.username,
            password=form_data.password,
        )

        if result is None:
            login_limiter.record_failure(limiter_key)
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        login_limiter.reset(limiter_key)
        return result

    except HTTPException:
        raise

    except Exception:
        logger.exception("Login request failed")
        raise HTTPException(
            status_code=503,
            detail="Authentication service temporarily unavailable",
        ) from None

    
@app.get(
    "/api/v1/auth/me",
    response_model=CurrentUserResponse,
    tags=["Authentication"],
)
def read_current_user(
    current_user: dict = Depends(get_current_user),
):
    try:
        profile = get_user_profile(current_user["user_id"])

    except Exception:
        logger.exception("Failed to load user profile")
        raise HTTPException(
            status_code=503,
            detail="Authentication service temporarily unavailable",
        ) from None

    if profile is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return profile


# --------------------------------------------------
# SECURITY INSPECTION
# Admin and Analyst access only
# --------------------------------------------------

@app.post(
    "/api/v1/inspect",
    response_model=InspectResponse,
    tags=["Inspection"],
)
def inspect_endpoint(
    request: InspectRequest,
    current_user: dict = Depends(
        require_roles("Admin", "Analyst")
    ),
):
    try:
        return inspect_and_store(
            application_id=request.application_id,
            endpoint_id=request.endpoint_id,
            text=request.text,
        )

    except ValueError as exc:
        if str(exc) in {
            "APPLICATION_NOT_FOUND_OR_INACTIVE",
            "ENDPOINT_NOT_FOUND_OR_INACTIVE",
        }:
            raise HTTPException(
                status_code=404,
                detail=str(exc),
            ) from exc

        raise HTTPException(
            status_code=400,
            detail="Invalid inspection request",
        ) from exc

    except Exception:
        logger.exception("Inspection request failed")

        raise HTTPException(
            status_code=503,
            detail="Inspection could not be completed",
        ) from None


# --------------------------------------------------
# ANALYTICS
# Admin, Analyst and Viewer access
# --------------------------------------------------

@app.get(
    "/api/v1/analytics/summary",
    tags=["Analytics"],
)
def analytics_summary(
    current_user: dict = Depends(
        require_roles("Admin", "Analyst", "Viewer")
    ),
):
    try:
        return get_security_summary()

    except Exception:
        logger.exception("Analytics summary query failed")

        raise HTTPException(
            status_code=503,
            detail="Analytics service temporarily unavailable",
        ) from None


# --------------------------------------------------
# SECURITY EVENTS
# Admin, Analyst and Viewer access
# --------------------------------------------------

@app.get(
    "/api/v1/events",
    tags=["Security Events"],
)
def list_security_events(
    limit: int = 50,
    current_user: dict = Depends(
        require_roles("Admin", "Analyst", "Viewer")
    ),
):
    if not 1 <= limit <= 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100",
        )

    try:
        events = get_recent_events(limit)

        return {
            "count": len(events),
            "events": events,
        }

    except Exception:
        logger.exception("Failed to retrieve security events")

        raise HTTPException(
            status_code=503,
            detail="Security events are temporarily unavailable",
        ) from None


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "PromptShield API is running",
        "docs": "/docs",
    }
