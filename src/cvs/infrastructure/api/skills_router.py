from fastapi import APIRouter, HTTPException, status
from src.cvs.application.create_skills import CreateSkill, CreateSkillCommand
from src.cvs.infrastructure.api.schemas import ResponseSchema, Detail, Data
from cvs.infrastructure.repositories import SQLModelSkillsRepository, SQLModelCvsRepository

skill_router = APIRouter(
    prefix="/cvs",
    tags=["Skills"],
)


@skill_router.post(
    "/skills/",
    response_model=ResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_skills(payload: dict):
    skill_repository = SQLModelSkillsRepository()
    cv_repository = SQLModelCvsRepository()
    create_skill_service = CreateSkill(skill_repository, cv_repository)

    try:
        cv_id = payload["cv_id"]
        skills = payload["skills"]

        response = create_skill_service.execute(
            CreateSkillCommand(cv_id=cv_id, skills=skills)
        )

        return ResponseSchema(
            detail=Detail(message="Skills saved successfully"),
            data=Data(cv_id=response.cv_id, description=response.get_skills()),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
