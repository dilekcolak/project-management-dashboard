from pydantic import BaseModel, Field, field_validator


class UserLogin(BaseModel):
    username: str = Field(
        min_length=1,
        max_length=50,
        examples=["dilekcolak"],
    )
    password: str = Field(
        min_length=1,
        max_length=128,
        examples=["StrongPassword123"],
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Username cannot be empty")

        return value


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600


class TokenPayload(BaseModel):
    sub: str
    user_id: int