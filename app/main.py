from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from .logger_conf import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("✅ Running")
    yield
    logger.info("❌ Turning off")


app = FastAPI(
    title="CV Generator API",
    description="API for generating ATS proof resumes",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello world!"}


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True, log_config=None)
