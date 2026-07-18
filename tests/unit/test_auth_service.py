from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth_service import register_user


def create_valid_user_data() -> UserCreate:
    return UserCreate(
        username="dilekcolak",
        email="dilek@example.com",
        password="Password123",
        repeat_password="Password123",
    )


@patch("app.services.auth_service.get_by_username")
def test_register_user_rejects_existing_username(
    mock_get_by_username: Mock,
) -> None:
    db = Mock(spec=Session)
    user_data = create_valid_user_data()
    mock_get_by_username.return_value = Mock(spec=User)

    with pytest.raises(HTTPException) as exception:
        register_user(
            db=db,
            user_data=user_data,
        )

    assert exception.value.status_code == 409
    assert exception.value.detail == "Username is already registered"


@patch("app.services.auth_service.get_by_email")
@patch("app.services.auth_service.get_by_username")
def test_register_user_rejects_existing_email(
    mock_get_by_username: Mock,
    mock_get_by_email: Mock,
) -> None:
    db = Mock(spec=Session)
    user_data = create_valid_user_data()

    mock_get_by_username.return_value = None
    mock_get_by_email.return_value = Mock(spec=User)

    with pytest.raises(HTTPException) as exception:
        register_user(
            db=db,
            user_data=user_data,
        )

    assert exception.value.status_code == 409
    assert exception.value.detail == "Email is already registered"


@patch("app.services.auth_service.create_user")
@patch("app.services.auth_service.hash_password")
@patch("app.services.auth_service.get_by_email")
@patch("app.services.auth_service.get_by_username")
def test_register_user_creates_user(
    mock_get_by_username: Mock,
    mock_get_by_email: Mock,
    mock_hash_password: Mock,
    mock_create_user: Mock,
) -> None:
    db = Mock(spec=Session)
    user_data = create_valid_user_data()
    created_user = Mock(spec=User)

    mock_get_by_username.return_value = None
    mock_get_by_email.return_value = None
    mock_hash_password.return_value = "hashed-password"
    mock_create_user.return_value = created_user

    result = register_user(
        db=db,
        user_data=user_data,
    )

    assert result is created_user

    mock_hash_password.assert_called_once_with("Password123")

    mock_create_user.assert_called_once_with(
        db=db,
        username="dilekcolak",
        email="dilek@example.com",
        hashed_password="hashed-password",
    )