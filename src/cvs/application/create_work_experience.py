from dataclasses import dataclass
from datetime import date
from cvs.domain.repositories import CvsRepository, WorkExperiencesRepository
from cvs.domain.models import WorkExperience
from src.cvs.domain.exceptions import CVDoesNotExist
from src.shared.domain.value_objects import Id


@dataclass
class CreateWECommand:
    cv_id: int
    role: str
    company_name: str
    summary: str
    start_date: date
    end_date: date


@dataclass
class CreateWEResponse:
    role: str
    company_name: str
    summary: str
    start_date: date
    end_date: date


class CreateWorkExperience:
    def __init__(
        self,
        work_experience_repository: WorkExperiencesRepository,
        cv_repository: CvsRepository,
    ):
        self._work_experience_repository = work_experience_repository
        self._cv_repository = cv_repository

    def execute(self, command: CreateWECommand) -> WorkExperience:
        id_object = Id(value=command.cv_id)
        if not self._cv_repository.exists_by_id(id_object):
            raise CVDoesNotExist(message=f"CV with id {command.cv_id} does not exist")

        work_experience = WorkExperience.create(
            cv_id=command.cv_id,
            role=command.role,
            company_name=command.company_name,
            summary=command.summary,
            start_date=command.start_date,
            end_date=command.end_date,
        )

        self._work_experience_repository.save(work_experience)

        return CreateWEResponse(
            role=work_experience.role(),
            company_name=work_experience.company_name(),
            summary=work_experience.summary(),
            start_date=work_experience.start_date(),
            end_date=work_experience.end_date(),
        )
