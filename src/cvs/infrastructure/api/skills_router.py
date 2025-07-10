from fastapi import APIRouter, HTTPException, status
from src.cvs.application.create_skills import CreateSkill, CreateSkillCommand
from src.cvs.domain.exceptions import CVDoesNotExist
from src.cvs.infrastructure.api.schemas import ResponseSchema, Detail, Data, SkillCreate
from cvs.infrastructure.repositories import (
    SQLModelSkillsRepository,
    SQLModelCvsRepository,
)
from src.shared.domain.value_objects import Id

skill_router = APIRouter(
    prefix="/cvs",
    tags=["Skills"],
)


@skill_router.post(
    "/skills/",
    response_model=ResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_skills(
    payload: SkillCreate,
):
    skill_repository = SQLModelSkillsRepository()
    cv_repository = SQLModelCvsRepository()
    create_skill_service = CreateSkill(skill_repository, cv_repository)

    try:
        cv = cv_repository.get_by_id(id=Id(value=payload.cv_id))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

    if cv is not None:
        try:
            cv_id = payload.cv_id
            skills = payload.skills

            response = create_skill_service.execute(
                CreateSkillCommand(cv_id=cv_id, skills=skills)
            )

            return ResponseSchema(
                detail=Detail(message="Skills saved successfully"),
                data=Data(
                    cv_id=cv.id,
                    user_id=cv.user_id,
                    description=response.skills,
                ),
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(CVDoesNotExist),
        )
