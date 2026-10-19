from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/")
def hello_world():
    return {"message": "Hello, Scrobitsss!"}


@router.get("/health")
def health():
    return {"status": "ok"}
