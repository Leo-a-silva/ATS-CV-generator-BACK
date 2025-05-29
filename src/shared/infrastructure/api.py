from fastapi import APIRouter, FastAPI, Request, Response

router = APIRouter()


@router.get("/health")
def check_health():
    return {"detail": "ok"}
