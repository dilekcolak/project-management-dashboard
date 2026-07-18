from unittest.mock import Mock

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repo import (
    create_user,
    get_by_email,
    get_by_username,
)


def test_get_by_username_returns_user() -> None:
    db = Mock(spec=Session)
    expected_user = Mock(spec=User)
    db.scalar.return_value = expected_user

    result = get_by_username(
        db=db,
        username="dilekcolak",
    )

    assert result is expected_user
    db.scalar.assert_called_once()


def test_get_by_username_returns_none_when_user_does_not_exist() -> None:
    db = Mock(spec=Session)
    db.scalar.return_value = None

    result = get_by_username(
        db=db,
        username="unknown",
    )

    assert result is None


def test_get_by_email_returns_user() -> None:
    db = Mock(spec=Session)
    expected_user = Mock(spec=User)
    db.scalar.return_value = expected_user

    result = get_by_email(
        db=db,
        email="dilek@example.com",
    )

    assert result is expected_user
    db.scalar.assert_called_once()


def test_create_user_saves_and_returns_user() -> None:
    db = Mock(spec=Session)

    result = create_user(
        db=db,
        username="dilekcolak",
        email="dilek@example.com",
        hashed_password="hashed-password",
    )

    assert isinstance(result, User)
    assert result.username == "dilekcolak"
    assert result.email == "dilek@example.com"
    assert result.hashed_password == "hashed-password"

    db.add.assert_called_once_with(result)
    db.commit.assert_called_once_with()
    db.refresh.assert_called_once_with(result)