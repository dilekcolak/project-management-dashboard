from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserResponse


def test_user_create_with_valid_data() -> None:
    user = UserCreate(
        username="dilekcolak",
        email="dilekcolak@gmail.com",
        password="sifre123",
        repeat_password="sifre123",
    )

    assert user.username == "dilekcolak"
    assert user.email == "dilekcolak@gmail.com"
    assert user.password == "sifre123"
    assert user.repeat_password == "sifre123"

def test_user_create_strips_username_whitespace() -> None:
    user = UserCreate(
        username="  dilekcolak  ",
        email="dilek@example.com",
        password="Password123",
        repeat_password="Password123",
    )

    assert user.username == "dilekcolak"

def test_user_create_rejects_empty_username() -> None:
    with pytest.raises(ValidationError, 
                       match="Username cannot be empty"
                    ):
        UserCreate(
            username="   ",
            email="dilek@example.com",
            password="Password123",
            repeat_password="Password123",
        )

def test_user_create_rejects_short_username() -> None:
    with pytest.raises(ValidationError):
        UserCreate(
            username="ab",
            email="dilek@example.com",
            password="Password123",
            repeat_password="Password123",
        )

def test_user_create_rejects_invalid_username_characters() -> None:
    with pytest.raises(
        ValidationError,
        match=
            "Username can only contain letters, numbers and underscores",
    ):
        UserCreate(
            username="dilek-colak",
            email="dilek@example.com",
            password="Password123",
            repeat_password="Password123",
        )

def test_user_create_accepts_underscore_in_username() -> None:
    user = UserCreate(
        username="dilek_colak",
        email="dilek@example.com",
        password="Password123",
        repeat_password="Password123",
    )

    assert user.username == "dilek_colak"

def test_user_create_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        UserCreate(
            username="dilekcolak",
            email="invalid-email",
            password="Password123",
            repeat_password="Password123",
        )

def test_user_create_rejects_short_password() -> None:
    with pytest.raises(ValidationError):
        UserCreate(
            username="dilekcolak",
            email="dilek@example.com",
            password="short",
            repeat_password="short",
        )

def test_user_create_rejects_non_matching_passwords() -> None:
    with pytest.raises(ValidationError, match="Passwords do not match"):
        UserCreate(
            username="dilekcolak",
            email="dilek@example.com",
            password="Password123",
            repeat_password="sifre123",
        )


def test_user_response_does_not_contain_password_fields() -> None:
    response = UserResponse(
        id=1,
        username="dilekcolak",
        email="dilek@example.com",
        created_at=datetime(2026, 7, 18, tzinfo=UTC),
    )

    response_data = response.model_dump()

    assert "password" not in response_data
    assert "repeat_password" not in response_data
    assert "hashed_password" not in response_data