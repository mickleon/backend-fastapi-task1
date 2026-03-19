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


class UserResponseSchema(UserBaseSchema):
    created_at: datetime = Field(description='Дата регистрации')

    model_config = ConfigDict(from_attributes=True)
