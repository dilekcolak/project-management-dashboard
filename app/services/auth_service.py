from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repo import (
    create_user,
    get_by_email,
    get_by_username,
)
from app.schemas.auth import TokenResponse, UserLogin
from app.schemas.user import UserCreate


def register_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    existing_username = get_by_username(
        db=db,
        username=user_data.username,
    )

    if existing_username is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already registered",
        )
    
    email = str(user_data.email)

    existing_email = get_by_email(
        db=db,
        email=email,
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    hashed_password = hash_password(user_data.password)

    return create_user(
        db=db,
        username=user_data.username,
        email=email,
        hashed_password=hashed_password,
    )


def login_user(
    db: Session,
    login_data: UserLogin,
) -> TokenResponse:
    user = get_by_username(
        db=db,
        username=login_data.username,
    )

    if user is None or not verify_password(
        login_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject=user.username,
        user_id=user.id,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=3600,
    )