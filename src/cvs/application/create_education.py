from dataclasses import dataclass
from datetime import date
from cvs.domain.repositories import (
    CvsRepository,
    EducationsRepository,
)
from cvs.domain.models import Education
from src.cvs.domain.exceptions import CVDoesNotExist
from src.shared.domain.value_objects import Id


@dataclass
class CreateEducationCommand:
    cv_id: int
    title: str
    institution: str
    start_date: date
    end_date: date


@dataclass
class CreateEducationResponse:
    title: str
    institution: str
    start_date: date
    end_date: date


class CreateEducation:
    def __init__(
        self,
        education_repository: EducationsRepository,
        cv_repository: CvsRepository,
    ):
        self._education_repository = education_repository
        self._cv_repository = cv_repository

    def execute(self, command: CreateEducationCommand) -> Education:
        id_object = Id(value=command.cv_id)
        if not self._cv_repository.exists_by_id(id_object):
            raise CVDoesNotExist(message=f"CV with id {command.cv_id} does not exist")

        education = Education.create(
            cv_id=command.cv_id,
            title=command.title,
            institution=command.institution,
            start_date=command.start_date,
            end_date=command.end_date,
        )

        self._education_repository.save(education)

        return CreateEducationResponse(
            title=education.title(),
            institution=education.institution(),
            start_date=education.start_date(),
            end_date=education.end_date(),
        )
