from fastapi import HTTPException, status
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
    field_validator,
)
from datetime import datetime


class UserBaseSchema(BaseModel):
    username: str = Field(max_length=64, description='Имя пользователя')
    email: EmailStr = Field(description='Email')

    first_name: str | None = Field(
        max_length=64, default=None, description='Имя'
    )
    last_name: str | None = Field(
        max_length=64, default=None, description='Фамилия'
    )

    is_active: bool = Field(default=True, description='Является активным')
    is_admin: bool = Field(
        default=False, description='Является администратором'
    )


class UserRequestSchema(UserBaseSchema):
    password: SecretStr = Field(min_length=8, description='Пароль')

    @field_validator('password', mode='after')
    @staticmethod
    def check_password(password: SecretStr) -> SecretStr:
        password_str = password.get_secret_value()
        has_upper = any(c.isupper() for c in password_str)
        has_lower = any(c.islower() for c in password_str)
        has_digit = any(c.isdigit() for c in password_str)
        has_special = any(not c.isalnum() for c in password_str)

        if not all([has_upper, has_lower, has_digit, has_special]):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Пароль должен содержать заглавные и строчные буквы, цифры и специальные символы',
            )
        return password


class UserResponseSchema(UserBaseSchema):
    created_at: datetime = Field(description='Дата регистрации')

    model_config = ConfigDict(from_attributes=True)
