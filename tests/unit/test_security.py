from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.schemas.auth import TokenPayload


def test_hash_password_does_not_return_plain_password() -> None:
    password = "Password123"

    hashed_password = hash_password(password)

    assert hashed_password != password


def test_hash_password_generates_different_hashes() -> None:
    password = "Password123"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash


def test_verify_password_returns_true_for_correct_password() -> None:
    password = "Password123"
    hashed_password = hash_password(password)

    result = verify_password(password, hashed_password)

    assert result is True


def test_verify_password_returns_false_for_incorrect_password() -> None:
    hashed_password = hash_password("Password123")

    result = verify_password("WrongPassword123", hashed_password)

    assert result is False

def test_decode_access_token_returns_token_payload() -> None:
    token = create_access_token(
        subject="dilekcolak",
        user_id=1,
    )

    payload = decode_access_token(token)

    assert isinstance(payload, TokenPayload)
    assert payload.sub == "dilekcolak"
    assert payload.user_id == 1