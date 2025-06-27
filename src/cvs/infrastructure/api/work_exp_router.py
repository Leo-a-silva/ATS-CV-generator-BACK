from typing import List
from fastapi import HTTPException, status, APIRouter

from src.cvs.application.create_work_experience import (
    CreateWECommand,
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
    response_model=List[WorkExperienceResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_work_experience(payload: List[WorkExperienceCreate]):
    we_repository = SQLModelWorkExperiencesRepository()
    cv_repository = SQLModelCvsRepository()
    create_work_exp_service = CreateWorkExperience(we_repository, cv_repository)

    responses: List[WorkExperienceResponse] = []
    for we_data in payload:
        try:
            we = create_work_exp_service.execute(
                CreateWECommand(
                    cv_id=we_data.cv_id,
                    role=we_data.role,
                    company_name=we_data.company_name,
                    summary=we_data.summary,
                    start_date=we_data.start_date,
                    end_date=we_data.end_date,
                )
            )
            responses.append(
                WorkExperienceResponse(
                    role=we.role,
                    company_name=we.company_name,
                    summary=we.summary,
                    start_date=we.start_date,
                    end_date=we.end_date,
                )
            )

        except CVDoesNotExist as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )

    return responses
