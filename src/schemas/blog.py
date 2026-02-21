from pydantic import BaseModel, EmailStr, Field, SecretStr, AnyUrl
from datetime import datetime


class User(BaseModel):
    username: str = Field(description='Имя пользователя')
    email: EmailStr = Field(description='Email')
    password: SecretStr = Field(min_length=8, description='Пароль')

    first_name: str | None = Field(default=None, description='Имя')
    last_name: str | None = Field(default=None, description='Фамилия')

    created_at: datetime = Field(
        default_factory=datetime.now, frozen=True, description='Дата регистрации'
    )
    is_active: bool = Field(default=True, description='Является активным')
    is_admin: bool = Field(default=False, description='Является администратором')


class BlogicumBaseModel(BaseModel):
    is_published: bool = Field(default=True, description='Опубликовано')
    created_at: datetime = Field(
        default_factory=datetime.now, frozen=True, description='Дата и время создания'
    )


class Category(BlogicumBaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    description: str = Field(description='Описание')
    slug: str = Field(
        pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$',
        max_length=64,
        description='Идентификатор категории в формате slug',
    )


class Location(BlogicumBaseModel):
    name: str = Field(max_length=256, description='Название места')


class Post(BlogicumBaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    text: str = Field(description='Текст')
    pub_date: datetime = Field(description='Дата и время публикации')

    author_id: int = Field(description='ID автора')
    location_id: int | None = Field(default=None, description='ID местоположения')
    category_id: int | None = Field(default=None, description='ID категории')
    image_url: AnyUrl | None = Field(
        default=None, description='URL прикрепленного изображения'
    )


class Comment(BaseModel):
    text: str = Field(description='Текст')
    post_id: int = Field(description='ID публикации')
    author_id: int = Field(description='ID автора')
    created_at: datetime = Field(
        default_factory=datetime.now, frozen=True, description='Дата и время создания'
    )
