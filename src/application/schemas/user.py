from fastapi import HTTPException, status
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)
from datetime import datetime
from application.resources.field_description import (
    USER_ID,
    USERNAME,
    EMAIL,
    FIRST_NAME,
    LAST_NAME,
    IS_ACTIVE,
    IS_ADMIN,
    PASSWORD,
)


class UserBaseSchema(BaseModel):
    username: str = Field(max_length=64, description=USERNAME)
    email: EmailStr = Field(description=EMAIL)

    first_name: str | None = Field(
        max_length=64, default=None, description=FIRST_NAME
    )
    last_name: str | None = Field(
        max_length=64, default=None, description=LAST_NAME
    )

    is_active: bool = Field(default=True, description=IS_ACTIVE)
    is_admin: bool = Field(default=False, description=IS_ADMIN)


class UserRequestSchema(UserBaseSchema):
    password: str = Field(min_length=8, description=PASSWORD)

    @field_validator('password', mode='after')
    @staticmethod
    def check_password(password: str) -> str:
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        if not all([has_upper, has_lower, has_digit, has_special]):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Пароль должен содержать заглавные и строчные буквы, цифры и специальные символы',
            )
        return password


class UserResponseSchema(UserBaseSchema):
    id: int = Field(description=USER_ID)
    created_at: datetime = Field(description='Дата регистрации')

    model_config = ConfigDict(from_attributes=True)
