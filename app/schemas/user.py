from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


class UserBase(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
        examples=["dilekcolak"]
    )

    email: EmailStr = Field(
        examples=["dilek@example.com"],
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Username cannot be empty")
        
        if not value.replace("_", "").isalnum():
            raise ValueError(
                "Username can only contain "
                "letters, numbers and underscores"
            )
        
        return value
    
class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=128,
        examples=["StrongPassword123"],
    )
    repeat_password: str = Field(
        min_length=8,
        max_length=128,
        examples=["StrongPassword123"],
    )

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "UserCreate":
        if self.password != self.repeat_password:
            raise ValueError("Passwords do not match")

        return self
    
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
