import stat
from fastapi import APIRouter, HTTPException, status

from cvs.application.create_cv import CreateCv, CreateCvCommand
from src.cvs.domain.exceptions import InvalidPhoneNumberException, InvalidUrlException
from src.cvs.infrastructure.schemas import CvCreate, CvResponse
from cvs.infrastructure.repositories import SQLModelCvsRepository
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
        return CvResponse.from_domain(cv)

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
