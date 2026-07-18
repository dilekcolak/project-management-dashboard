from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repo import (
    create_user,
    get_by_email,
    get_by_username,
)
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