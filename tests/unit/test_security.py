from app.core.security import hash_password, verify_password


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