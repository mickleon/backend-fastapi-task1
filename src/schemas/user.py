from pydantic import BaseModel, EmailStr, Field, SecretStr
from datetime import datetime


class UserRequestSchema(BaseModel):
    username: str = Field(description='Имя пользователя')
    email: EmailStr = Field(description='Email')
    password: SecretStr = Field(min_length=8, description='Пароль')

    first_name: str | None = Field(default=None, description='Имя')
    last_name: str | None = Field(default=None, description='Фамилия')


class UserResponseSchema(BaseModel):
    username: str = Field(description='Имя пользователя')
    email: EmailStr = Field(description='Email')

    first_name: str | None = Field(default=None, description='Имя')
    last_name: str | None = Field(default=None, description='Фамилия')

    created_at: datetime = Field(description='Дата регистрации')
    is_active: bool = Field(description='Является активным')
    is_admin: bool = Field(description='Является администратором')
