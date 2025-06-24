from fastapi import HTTPException, status, APIRouter

from cvs.application.create_cv import CreateCv, CreateCvCommand
from src.cvs.domain.exceptions import (
    InvalidPhoneNumberException,
    InvalidUrlException,
)
from src.cvs.infrastructure.api.schemas import (
    CvCreate,
    CvResponse,
)
from cvs.infrastructure.repositories import (
    SQLModelCvsRepository,
)
from src.shared.domain.exceptions import InvalidEmailAddressException
from src.users.domain.exceptions import UserDoesNotExist
from src.users.infrastructure.repositories import SQLModelUsersRepository

cv_router = APIRouter(
    prefix="/cvs",
    tags=["CVs"],
)


@cv_router.post(
    "/create/",
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
