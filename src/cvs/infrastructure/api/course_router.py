from typing import List
from fastapi import Depends, HTTPException, status, APIRouter

from src.cvs.application.create_course import (
    CreateCourse,
    CreateCourseCommand,
)
from src.cvs.domain.exceptions import (
    CVDoesNotExist,
)
from src.cvs.infrastructure.api.schemas import (
    Data,
    Detail,
    CourseBase,
    CourseCreate,
    ResponseSchema,
)
from cvs.infrastructure.repositories import (
    SQLModelCvsRepository,
    SQLModelCoursesRepository,
)
from src.shared.domain.value_objects import Id
from src.users.infrastructure.api.dependencies import get_current_user_id

course_router = APIRouter(
    prefix="/cvs",
    tags=["Courses"],
)


@course_router.post(
    "/course/",
    response_model=ResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Requiere autenticación JWT. Enviar el token en el header: Authorization: Bearer <token>",

)
def create_course(
    payload: CourseCreate,
    current_user_id: int = Depends(get_current_user_id),
):
    course_repository = SQLModelCoursesRepository()
    cv_repository = SQLModelCvsRepository()
    create_course_service = CreateCourse(course_repository, cv_repository)

    try:
        cv = cv_repository.get_by_id(id=Id(value=payload.cv_id))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

    if cv is not None:
        courses: List[CourseBase] = []

        for course in payload.courses:
            try:
                new_course = create_course_service.execute(
                    CreateCourseCommand(
                        cv_id=cv.id,
                        title=course.title,
                        institution=course.institution,
                        start_date=course.start_date,
                    )
                )
                courses.append(
                    CourseBase(
                        title=new_course.title,
                        institution=new_course.institution,
                        start_date=new_course.start_date,
                    )
                )

            except CVDoesNotExist as e:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
                )

        return ResponseSchema(
            detail=Detail(
                message="Courses saved succesfully",
            ),
            data=Data(
                cv_id=cv.id,
                user_id=cv.user_id,
                description=courses,
            ),
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(CVDoesNotExist),
        )
