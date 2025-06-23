from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel
from shared.infrastructure.api import router as shared_router
from src.cvs.infrastructure.routes import router as cvs_router
from src.shared.domain.exceptions import InvalidEmailAddressException
from users.infrastructure.api.routes import router as users_router
from shared.infrastructure.logger_conf import logger
from shared.infrastructure.db_conf import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("✅ Running")
    SQLModel.metadata.create_all(engine)
    yield
    logger.info("❌ Turning off")


app = FastAPI(
    title="CV Generator API",
    summary="API for generating ATS proof resumes",
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(InvalidEmailAddressException)
async def invalid_email_exception_handler(
    request: Request, exc: InvalidEmailAddressException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": [{"msg": str(exc), "type": "invalid_email"}]},
    )


app.include_router(shared_router, prefix="/api")
app.include_router(cvs_router, prefix="/api", tags=["CVs"])
app.include_router(users_router, prefix="/api", tags=["Users"])
