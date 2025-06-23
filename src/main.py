from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from shared.infrastructure.api import router as shared_router
from cvs.infrastructure.api import router as cvs_router
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


app.include_router(shared_router, prefix="/api")
app.include_router(cvs_router, prefix="/api", tags=["CVs"])
app.include_router(users_router, prefix="/api", tags=["Users"])
