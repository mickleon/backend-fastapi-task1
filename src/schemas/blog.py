from pydantic import BaseModel, EmailStr, Field, SecretStr, AnyUrl
from datetime import datetime

SLUG_PATTERN: str = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'


# User


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


# Category


class CategoryRequestSchema(BaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    description: str = Field(description='Описание')
    slug: str = Field(
        pattern=SLUG_PATTERN,
        max_length=64,
        description='Идентификатор категории в формате slug',
    )

    is_published: bool = Field(default=True, description='Опубликовано')


class CategoryResponseSchema(BaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    description: str = Field(description='Описание')
    slug: str = Field(
        pattern=SLUG_PATTERN,
        max_length=64,
        description='Идентификатор категории в формате slug',
    )

    is_published: bool = Field(default=True, description='Опубликовано')
    created_at: datetime = Field(description='Дата и время создания')


# Location


class LocationRequestSchema(BaseModel):
    name: str = Field(max_length=256, description='Название места')
    is_published: bool = Field(default=True, description='Опубликовано')


class LocationResponseSchema(BaseModel):
    name: str = Field(max_length=256, description='Название места')

    is_published: bool = Field(default=True, description='Опубликовано')
    created_at: datetime = Field(description='Дата и время создания')


# Post


class PostRequestSchema(BaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    text: str = Field(description='Текст')
    pub_date: datetime = Field(description='Дата и время публикации')

    location_id: int | None = Field(default=None, description='ID местоположения')
    category_id: int | None = Field(default=None, description='ID категории')
    image_url: AnyUrl | None = Field(
        default=None, description='URL прикрепленного изображения'
    )

    is_published: bool = Field(default=True, description='Опубликовано')


class PostResponseSchema(BaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    text: str = Field(description='Текст')
    pub_date: datetime = Field(description='Дата и время публикации')

    author_id: int = Field(description='ID автора')
    location_id: int | None = Field(default=None, description='ID местоположения')
    category_id: int | None = Field(default=None, description='ID категории')
    image_url: AnyUrl | None = Field(
        default=None, description='URL прикрепленного изображения'
    )

    is_published: bool = Field(default=True, description='Опубликовано')
    created_at: datetime = Field(description='Дата и время создания')


# Comment


class CommentRequestSchema(BaseModel):
    text: str = Field(description='Текст')
    post_id: int = Field(description='ID публикации')


class CommentResponseSchema(BaseModel):
    text: str = Field(description='Текст')
    post_id: int = Field(description='ID публикации')
    author_id: int = Field(description='ID автора')
    created_at: datetime = Field(description='Дата и время создания')
