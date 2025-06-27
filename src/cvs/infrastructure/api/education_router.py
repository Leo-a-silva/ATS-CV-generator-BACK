from typing import List
from fastapi import HTTPException, status, APIRouter

from src.cvs.application.create_education import (
    CreateEducation,
    CreateEducationCommand,
)
from src.cvs.domain.exceptions import (
    CVDoesNotExist,
)
from src.cvs.infrastructure.api.schemas import (
    EducationCreate,
    EducationResponse,
)
from cvs.infrastructure.repositories import (
    SQLModelCvsRepository,
    SQLModelEducationsRepository,
)

education_router = APIRouter(
    prefix="/cvs",
    tags=["Educations"],
)


@education_router.post(
    "/education/",
    response_model=List[EducationResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_education(payload: List[EducationCreate]):
    education_repository = SQLModelEducationsRepository()
    cv_repository = SQLModelCvsRepository()
    create_education_service = CreateEducation(education_repository, cv_repository)

    responses: List[EducationResponse] = []
    for edu in payload:
        try:
            education = create_education_service.execute(
                CreateEducationCommand(
                    cv_id=edu.cv_id,
                    title=edu.title,
                    institution=edu.institution,
                    start_date=edu.start_date,
                    end_date=edu.end_date,
                )
            )
            responses.append(
                EducationResponse(
                    title=education.title,
                    institution=education.institution,
                    start_date=education.start_date,
                    end_date=education.end_date,
                )
            )

        except CVDoesNotExist as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )
    return responses
