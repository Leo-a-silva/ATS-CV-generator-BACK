from typing import List
from fastapi import Depends, HTTPException, status, APIRouter

from src.cvs.application.create_education import (
    CreateEducation,
    CreateEducationCommand,
)
from src.cvs.domain.exceptions import (
    CVDoesNotExist,
)
from src.cvs.infrastructure.api.schemas import (
    Data,
    Detail,
    EducationBase,
    EducationCreate,
    ResponseSchema,
)
from cvs.infrastructure.repositories import (
    SQLModelCvsRepository,
    SQLModelEducationsRepository,
)
from src.shared.domain.value_objects import Id
from src.users.infrastructure.api.dependencies import get_current_user_id

education_router = APIRouter(
    prefix="/cvs",
    tags=["Educations"],
)


@education_router.post(
    "/education/",
    response_model=ResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Requiere autenticación JWT. Enviar el token en el header: Authorization: Bearer <token>",

)
def create_education(
    payload: EducationCreate,
    current_user_id: int = Depends(get_current_user_id),
):
    education_repository = SQLModelEducationsRepository()
    cv_repository = SQLModelCvsRepository()
    create_education_service = CreateEducation(education_repository, cv_repository)

    try:
        cv = cv_repository.get_by_id(id=Id(value=payload.cv_id))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

    if cv is not None:
        educations: List[EducationBase] = []

        for edu in payload.educations:
            try:
                education = create_education_service.execute(
                    CreateEducationCommand(
                        cv_id=cv.id,
                        title=edu.title,
                        institution=edu.institution,
                        start_date=edu.start_date,
                        end_date=edu.end_date,
                    )
                )
                educations.append(
                    EducationBase(
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

        return ResponseSchema(
            detail=Detail(
                message="Educations saved succesfully",
            ),
            data=Data(
                cv_id=cv.id,
                user_id=cv.user_id,
                description=educations,
            ),
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(CVDoesNotExist),
        )
