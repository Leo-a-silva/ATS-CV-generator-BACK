from fastapi import APIRouter
from src.cvs.infrastructure.api.course_router import course_router
from src.cvs.infrastructure.api.cv_router import cv_router
from src.cvs.infrastructure.api.education_router import education_router
from src.cvs.infrastructure.api.work_exp_router import we_router

router = APIRouter()

router.include_router(cv_router)
router.include_router(we_router)
router.include_router(education_router)
router.include_router(course_router)
