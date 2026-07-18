import pytest
from pydantic import ValidationError

from app.schemas.auth import TokenPayload, TokenResponse, UserLogin


def test_user_login_with_valid_data() -> None:
    login = UserLogin(
        username="dilekcolak",
        password="Password123",
    )

    assert login.username == "dilekcolak"
    assert login.password == "Password123"


def test_user_login_strips_username_whitespace() -> None:
    login = UserLogin(
        username="  dilekcolak  ",
        password="Password123",
    )

    assert login.username == "dilekcolak"


def test_user_login_rejects_empty_username() -> None:
    with pytest.raises(ValidationError, match="Username cannot be empty"):
        UserLogin(
            username="   ",
            password="Password123",
        )


def test_user_login_rejects_empty_password() -> None:
    with pytest.raises(ValidationError):
        UserLogin(
            username="dilekcolak",
            password="",
        )


def test_token_response_uses_default_values() -> None:
    token = TokenResponse(access_token="encoded.jwt.token")

    assert token.access_token == "encoded.jwt.token"
    assert token.token_type == "bearer"
    assert token.expires_in == 3600


def test_token_response_accepts_explicit_values() -> None:
    token = TokenResponse(
        access_token="encoded.jwt.token",
        token_type="bearer",
        expires_in=1800,
    )

    assert token.expires_in == 1800


def test_token_payload_with_valid_data() -> None:
    payload = TokenPayload(
        sub="dilekcolak",
        user_id=1,
    )

    assert payload.sub == "dilekcolak"
    assert payload.user_id == 1


def test_token_payload_rejects_missing_user_id() -> None:
    with pytest.raises(ValidationError):
        TokenPayload(sub="dilekcolak")  # type: ignore[call-arg]