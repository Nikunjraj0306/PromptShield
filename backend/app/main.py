from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

from app.database import check_database_connection

from fastapi import HTTPException, status
from app.schemas import InspectRequest, InspectResponse
from app.inspection_service import inspect_and_store

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
        raise HTTPException(
            status_code=503,
            detail="Database is unavailable",
        )


@app.post(
    "/api/v1/inspect",
    response_model=InspectResponse,
    tags=["Inspection"],
)
def inspect_endpoint(request: InspectRequest):
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
        raise HTTPException(
            status_code=503,
            detail="Inspection could not be completed",
        )

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "PromptShield API is running",
        "docs": "/docs",
    }
