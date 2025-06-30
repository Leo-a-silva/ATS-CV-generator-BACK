from curses.ascii import HT
from fastapi import APIRouter, HTTPException, status
from src.shared.domain.exceptions import InvalidEmailAddressException
from src.users.application.use_cases.login_user import (
    LoginUserCommand,
    LoginUserResponse,
    LoginUserUseCase,
)
from src.users.application.use_cases.register_user import (
    RegisterUserCommand,
    RegisterUserUseCase,
)
from src.users.domain.exceptions import (
    PasswordDoesNotMatch,
    UserAlreadyExistsException,
    UserDoesNotExist,
)
from src.users.infrastructure.api.schemas import (
    LoginUserRequest,
    RegisterUserRequest,
    UserResponse,
)
from src.users.infrastructure.repositories import SQLModelUsersRepository
from src.users.infrastructure.services import BcryptPasswordHashingService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/login/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def login_user(payload: LoginUserRequest) -> UserResponse:
    try:
        users_repository = SQLModelUsersRepository()
        password_service = BcryptPasswordHashingService()
        use_case = LoginUserUseCase(users_repository, password_service)

        user = use_case.execute(
            LoginUserCommand(
                email_address=payload.email_address,
                password=payload.password,
            )
        )

        return UserResponse(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email_address=user.email_address,
            created_at=user.created_at,
        )

    except InvalidEmailAddressException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

    except UserDoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except PasswordDoesNotMatch as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post(
    "/register/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    payload: RegisterUserRequest,
) -> UserResponse:
    try:
        users_repository = SQLModelUsersRepository()
        password_service = BcryptPasswordHashingService()
        use_case = RegisterUserUseCase(users_repository, password_service)

        user = use_case.execute(
            RegisterUserCommand(
                first_name=payload.first_name,
                last_name=payload.last_name,
                email_address=payload.email_address,
                password=payload.password,
            )
        )

        return UserResponse(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email_address=user.email_address,
            created_at=user.created_at,
        )

    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except InvalidEmailAddressException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
