from dataclasses import dataclass
from datetime import date
from cvs.domain.repositories import (
    CvsRepository,
    CoursesRepository,
)
from cvs.domain.models import Course
from src.cvs.domain.exceptions import CVDoesNotExist
from src.shared.domain.value_objects import Id


@dataclass
class CreateCourseCommand:
    cv_id: int
    title: str
    institution: str
    start_date: date


@dataclass
class CreateCourseResponse:
    title: str
    institution: str
    start_date: date


class CreateCourse:
    def __init__(
        self,
        course_repository: CoursesRepository,
        cv_repository: CvsRepository,
    ):
        self._course_repository = course_repository
        self._cv_repository = cv_repository

    def execute(self, command: CreateCourseCommand) -> Course:
        id_object = Id(value=command.cv_id)
        if not self._cv_repository.exists_by_id(id_object):
            raise CVDoesNotExist(message=f"CV with id {command.cv_id} does not exist")

        education = Course.create(
            cv_id=command.cv_id,
            title=command.title,
            institution=command.institution,
            start_date=command.start_date,
        )

        self._course_repository.save(education)

        return CreateCourseResponse(
            title=education.title(),
            institution=education.institution(),
            start_date=education.start_date(),
        )
