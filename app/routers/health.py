"""
Health / hello routes.

APIRouter = a mini-app you later attach to the main FastAPI app.
tags=... only groups endpoints in /docs (does not change URLs).

These stay as normal `def` (not async) — no DB I/O to wait on.
That is fine in FastAPI. Use async where you actually await something.
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
def hello_world():
    # @router.get("/") is a DECORATOR:
    # "when someone GETs /, run this function"
    return {"message": "Hello, Scrobitsss!"}


@router.get("/health")
def health():
    return {"status": "ok"}
