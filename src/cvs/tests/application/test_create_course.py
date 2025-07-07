from src.cvs.application.create_cv import CreateCv, CreateCvCommand
from src.cvs.application.create_course import CreateCourseCommand, CreateCourse
from src.cvs.tests.application.fake_repositories import (
    FakeCvRepository,
    FakeCourseRepository,
    FakeUsersRepository,
)


class TestCreateEducation:
    def test_creates_education_with_all_fields(self) -> None:
        cv_repository = FakeCvRepository()
        users_repository = FakeUsersRepository()
        courses_repository = FakeCourseRepository()

        new_user = {
            "id": 1,
            "first_name": "Steve",
            "last_name": "Jobs",
            "email_address": "steve.jobs@example.com",
            "hashed_password": "MyHashedPassword123",
            "created_at": "2025-06-23 16:45:48",
            "updated_at": "2025-06-23 16:45:48",
        }
        users_repository.save(new_user)

        CreateCv(cv_repository, users_repository).execute(
            CreateCvCommand(
                user_id=1,
                first_name="Steve",
                last_name="Jobs",
                email_address="steve.jobs@example.com",
                phone_number="+543434586789",
                linkedin_url="https://linkedin.com/",
                portfolio_url="https://ats.com/",
                country="ARG",
                city="Buenos Aires",
                summary="Star",
            )
        )

        CreateCourse(courses_repository, cv_repository).execute(
            CreateCourseCommand(
                cv_id=1,
                title="CS50 Machine Learning with Python",
                institution="Hardvard",
                start_date="2022-09-28",
            )
        )
        CreateCourse(courses_repository, cv_repository).execute(
            CreateCourseCommand(
                cv_id=1,
                title="AWS Cloud Practitioner",
                institution="Udemy",
                start_date="2024-03-18",
            )
        )

        courses = courses_repository.all_by_cv_id(id=1)
        assert len(courses) == 2
        course = courses[1]
        assert course.title() == "AWS Cloud Practitioner"
        assert course.cv_id() == 1
