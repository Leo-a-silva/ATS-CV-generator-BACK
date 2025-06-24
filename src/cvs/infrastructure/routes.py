from fastapi import APIRouter, HTTPException, status

from cvs.application.create_cv import CreateCv, CreateCvCommand
from src.cvs.application.create_work_experience import (
    CreateWECommand,
    CreateWEResponse,
    CreateWorkExperience,
)
from src.cvs.domain.exceptions import (
    CVDoesNotExist,
    InvalidPhoneNumberException,
    InvalidUrlException,
)
from src.cvs.infrastructure.schemas import (
    CvCreate,
    CvResponse,
    WorkExperienceCreate,
    WorkExperienceResponse,
)
from cvs.infrastructure.repositories import (
    SQLModelCvsRepository,
    SQLModelWorkExperiencesRepository,
)
from src.shared.domain.exceptions import InvalidEmailAddressException
from src.users.domain.exceptions import UserDoesNotExist
from src.users.infrastructure.repositories import SQLModelUsersRepository

router = APIRouter()


@router.post(
    "/cvs/",
    response_model=CvResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_cv(payload: CvCreate):
    cvs_repository = SQLModelCvsRepository()
    users_repository = SQLModelUsersRepository()

    try:
        create_cv_service = CreateCv(cvs_repository, users_repository)

        cv = create_cv_service.execute(
            CreateCvCommand(
                user_id=payload.user_id,
                first_name=payload.first_name,
                last_name=payload.last_name,
                email_address=payload.email_address,
                phone_number=payload.phone_number,
                linkedin_url=payload.linkedin_url,
                portfolio_url=payload.portfolio_url,
                country=payload.country,
                city=payload.city,
                summary=payload.summary,
            )
        )
        return CvResponse(
            cv_id=cv.cv_id,
            user_id=cv.user_id,
            first_name=cv.first_name,
            last_name=cv.last_name,
            email_address=cv.email_address,
            phone_number=cv.phone_number,
            linkedin_url=cv.linkedin_url,
            portfolio_url=cv.portfolio_url,
            country=cv.country,
            city=cv.city,
            summary=cv.summary,
        )

    except UserDoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

    except InvalidPhoneNumberException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

    except InvalidEmailAddressException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

    except InvalidUrlException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.post(
    "/cvs/work-experience/",
    response_model=WorkExperienceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_work_experience(payload: WorkExperienceCreate):
    we_repository = SQLModelWorkExperiencesRepository()
    cv_repository = SQLModelCvsRepository()

    try:
        create_work_exp_service = CreateWorkExperience(we_repository, cv_repository)

        we = create_work_exp_service.execute(
            CreateWECommand(
                cv_id=payload.cv_id,
                role=payload.role,
                company_name=payload.company_name,
                summary=payload.summary,
                start_date=payload.start_date,
                end_date=payload.end_date,
            )
        )
        return CreateWEResponse(
            role=we.role,
            company_name=we.company_name,
            summary=we.summary,
            start_date=we.start_date,
            end_date=we.end_date,
        )

    except CVDoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
