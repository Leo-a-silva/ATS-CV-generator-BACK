from fastapi import FastAPI
from shared.infrastructure.api import router as shared_router
from cvs.infrastructure.api import router as cvs_router

app = FastAPI()

app.include_router(shared_router)
app.include_router(cvs_router)
