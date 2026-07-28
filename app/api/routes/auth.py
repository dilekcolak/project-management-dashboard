from fastapi import APIRouter, status

from app.api.dependencies import DatabaseSession
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLogin
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import login_user, register_user

router = APIRouter(
    tags=["Authentication"],
)

@router.post(
    "/auth",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    db: DatabaseSession,
) -> User:
    return register_user(
        db=db,
        user_data=user_data,
    )

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    login_data: UserLogin,
    db: DatabaseSession,
) -> TokenResponse:
    return login_user(
        db=db,
        login_data=login_data,
    )

