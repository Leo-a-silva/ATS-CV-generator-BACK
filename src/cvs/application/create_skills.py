from dataclasses import dataclass
from cvs.domain.repositories import CvsRepository, SkillsRepository
from cvs.domain.models import Skill
from src.cvs.domain.exceptions import CVDoesNotExist
from src.shared.domain.value_objects import Id


@dataclass
class CreateSkillCommand:
    cv_id: int
    skills: list[str]  # List of skills as strings


@dataclass
class CreateSkillResponse:
    cv_id: int
    skills: list[str]


class CreateSkill:
    def __init__(
        self,
        skill_repository: SkillsRepository,
        cv_repository: CvsRepository,
    ):
        self._skill_repository = skill_repository
        self._cv_repository = cv_repository

    def execute(self, command: CreateSkillCommand) -> Skill:
        id_object = Id(value=command.cv_id)
        if not self._cv_repository.exists_by_id(id_object):
            raise CVDoesNotExist(message=f"CV with id {command.cv_id} does not exist")

        skill = Skill.create(
            cv_id=command.cv_id,
            skills=command.skills,
        )

        self._skill_repository.save(skill)

        return CreateSkillResponse(
            cv_id=skill.cv_id(),
            skills=skill.get_skills(),
        )
