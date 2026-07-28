from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException
from jose import JWTError
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import TokenPayload


@patch("app.api.dependencies.get_by_id")
@patch("app.api.dependencies.decode_access_token")
def test_get_current_user_returns_user_for_valid_token(
    mock_decode_access_token: Mock,
    mock_get_by_id: Mock,
) -> None:
    db = Mock(spec=Session)

    payload = TokenPayload(
        sub="dilekcolak",
        user_id=1,
        exp=1785220000,
    )
    expected_user = User(
        username="dilekcolak",
        email="dilek@example.com",
        hashed_password="hashed-password",
    )

    mock_decode_access_token.return_value = payload
    mock_get_by_id.return_value = expected_user

    result = get_current_user(
        token="valid-token",
        db=db,
    )

    assert result is expected_user

    mock_decode_access_token.assert_called_once_with(
        "valid-token",
    )
    mock_get_by_id.assert_called_once_with(
        db=db,
        user_id=1,
    )

@patch("app.api.dependencies.decode_access_token")
def test_get_current_user_raises_401_for_invalid_token(
    mock_decode_access_token: Mock,
) -> None:
    db = Mock(spec=Session)
    mock_decode_access_token.side_effect = JWTError()

    with pytest.raises(HTTPException) as exception_info:
        get_current_user(
            token="invalid-token",
            db=db,
        )

    assert exception_info.value.status_code == 401
    assert (
        exception_info.value.detail
        == "Could not validate credentials"
    )
    assert exception_info.value.headers == {
        "WWW-Authenticate": "Bearer",
    }

@patch("app.api.dependencies.get_by_id")
@patch("app.api.dependencies.decode_access_token")
def test_get_current_user_raises_401_when_user_does_not_exist(
    mock_decode_access_token: Mock,
    mock_get_by_id: Mock,
) -> None:
    db = Mock(spec=Session)

    mock_decode_access_token.return_value = TokenPayload(
        sub="deleted-user",
        user_id=999,
        exp=1785220000,
    )
    mock_get_by_id.return_value = None

    with pytest.raises(HTTPException) as exception_info:
        get_current_user(
            token="valid-token",
            db=db,
        )

    assert exception_info.value.status_code == 401
    assert (
        exception_info.value.detail
        == "Could not validate credentials"
    )

    mock_get_by_id.assert_called_once_with(
        db=db,
        user_id=999,
    )