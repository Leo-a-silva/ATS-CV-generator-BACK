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
    Data,
    Detail,
    ResponseSchema,
    WorkExperienceBase,
    WorkExperienceCreate,
)
from cvs.infrastructure.repositories import (
    SQLModelCvsRepository,
    SQLModelWorkExperiencesRepository,
)
from src.shared.domain.value_objects import Id

we_router = APIRouter(
    prefix="/cvs",
    tags=["Work Experiences"],
)


@we_router.post(
    "/work-experience/",
    response_model=ResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_work_experience(payload: WorkExperienceCreate):
    we_repository = SQLModelWorkExperiencesRepository()
    cv_repository = SQLModelCvsRepository()
    create_work_exp_service = CreateWorkExperience(we_repository, cv_repository)

    try:
        cv = cv_repository.get_by_id(id=Id(value=payload.cv_id))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

    if cv is not None:
        work_experiences: List[WorkExperienceBase] = []

        for we_data in payload.work_experiences:
            try:
                we = create_work_exp_service.execute(
                    CreateWECommand(
                        cv_id=cv.id,
                        role=we_data.role,
                        company_name=we_data.company_name,
                        summary=we_data.summary,
                        start_date=we_data.start_date,
                        end_date=we_data.end_date,
                    )
                )
                work_experiences.append(
                    WorkExperienceBase(
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

        return ResponseSchema(
            detail=Detail(
                message="Work Experiences saved succesfully",
            ),
            data=Data(
                cv_id=cv.id,
                user_id=cv.user_id,
                description=work_experiences,
            ),
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(CVDoesNotExist),
        )
