from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_by_username(
    db: Session,
    username: str,
) -> User | None:
    statement = select(User).where(
        User.username == username,
    )

    return db.scalar(statement)


def get_by_email(
    db: Session,
    email: str,
) -> User | None:
    statement = select(User).where(
        User.email == email,
    )

    return db.scalar(statement)


def create_user(
    db: Session,
    username: str,
    email: str,
    hashed_password: str,
) -> User:
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user