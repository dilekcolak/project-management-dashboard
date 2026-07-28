from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import TokenResponse, UserLogin
from app.services.auth_service import login_user


def create_login_data() -> UserLogin:
    return UserLogin(
        username="dilekcolak",
        password="Password123",
    )


@patch("app.services.auth_service.get_by_username")
def test_login_rejects_unknown_user(
    mock_get_by_username: Mock,
) -> None:
    db = Mock(spec=Session)
    login_data = create_login_data()

    mock_get_by_username.return_value = None

    with pytest.raises(HTTPException) as exception:
        login_user(
            db=db,
            login_data=login_data,
        )

    assert exception.value.status_code == 401
    assert exception.value.detail == "Invalid username or password"


@patch("app.services.auth_service.verify_password")
@patch("app.services.auth_service.get_by_username")
def test_login_rejects_invalid_password(
    mock_get_by_username: Mock,
    mock_verify_password: Mock,
) -> None:
    db = Mock(spec=Session)
    login_data = create_login_data()
    user = Mock(spec=User)
    user.hashed_password = "hashed-password"

    mock_get_by_username.return_value = user
    mock_verify_password.return_value = False

    with pytest.raises(HTTPException) as exception:
        login_user(
            db=db,
            login_data=login_data,
        )

    assert exception.value.status_code == 401
    assert exception.value.detail == "Invalid username or password"

    mock_verify_password.assert_called_once_with(
        "Password123",
        "hashed-password",
    )


@patch("app.services.auth_service.create_access_token")
@patch("app.services.auth_service.verify_password")
@patch("app.services.auth_service.get_by_username")
def test_login_returns_access_token(
    mock_get_by_username: Mock,
    mock_verify_password: Mock,
    mock_create_access_token: Mock,
) -> None:
    db = Mock(spec=Session)
    login_data = create_login_data()

    user = Mock(spec=User)
    user.id = 1
    user.username = "dilekcolak"
    user.hashed_password = "hashed-password"

    mock_get_by_username.return_value = user
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "jwt-token"

    result = login_user(
        db=db,
        login_data=login_data,
    )

    assert result == TokenResponse(
        access_token="jwt-token",
        token_type="bearer",
        expires_in=3600,
    )

    mock_verify_password.assert_called_once_with(
        "Password123",
        "hashed-password",
    )
    mock_create_access_token.assert_called_once_with(
        subject="dilekcolak",
        user_id=1,
    )