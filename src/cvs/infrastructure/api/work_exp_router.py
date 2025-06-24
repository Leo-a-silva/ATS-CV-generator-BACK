from fastapi import HTTPException, status, APIRouter

from src.cvs.application.create_work_experience import (
    CreateWECommand,
    CreateWEResponse,
    CreateWorkExperience,
)
from src.cvs.domain.exceptions import (
    CVDoesNotExist,
)
from src.cvs.infrastructure.api.schemas import (
    WorkExperienceCreate,
    WorkExperienceResponse,
)
from cvs.infrastructure.repositories import (
    SQLModelCvsRepository,
    SQLModelWorkExperiencesRepository,
)

we_router = APIRouter(
    prefix="/cvs",
    tags=["Work Experiences"],
)


@we_router.post(
    "/work-experience/",
    response_model=WorkExperienceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_work_experience(payload: WorkExperienceCreate):
    we_repository = SQLModelWorkExperiencesRepository()
    cv_repository = SQLModelCvsRepository()

    try:
        create_work_exp_service = CreateWorkExperience(we_repository, cv_repository)

        we = create_work_exp_service.execute(
            CreateWECommand(
                cv_id=payload.cv_id,
                role=payload.role,
                company_name=payload.company_name,
                summary=payload.summary,
                start_date=payload.start_date,
                end_date=payload.end_date,
            )
        )
        return CreateWEResponse(
            role=we.role,
            company_name=we.company_name,
            summary=we.summary,
            start_date=we.start_date,
            end_date=we.end_date,
        )

    except CVDoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
