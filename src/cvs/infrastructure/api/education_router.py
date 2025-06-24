from fastapi import HTTPException, status, APIRouter

from src.cvs.application.create_education import (
    CreateEducation,
    CreateEducationCommand,
    CreateEducationResponse,
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
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_education(payload: EducationCreate):
    education_repository = SQLModelEducationsRepository()
    cv_repository = SQLModelCvsRepository()

    try:
        create_education_service = CreateEducation(education_repository, cv_repository)

        education = create_education_service.execute(
            CreateEducationCommand(
                cv_id=payload.cv_id,
                title=payload.title,
                institution=payload.institution,
                start_date=payload.start_date,
                end_date=payload.end_date,
            )
        )
        return CreateEducationResponse(
            title=education.title,
            institution=education.institution,
            start_date=education.start_date,
            end_date=education.end_date,
        )

    except CVDoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
