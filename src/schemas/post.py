import uuid
from pydantic import BaseModel, Field, AnyUrl, ConfigDict
from datetime import datetime


class PostRequestSchema(BaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    text: str = Field(description='Текст')
    pub_date: datetime = Field(description='Дата и время публикации')

    author_id: int = Field(description='ID автора')
    location_id: uuid.UUID | None = Field(
        default=None, description='ID местоположения'
    )
    category_id: uuid.UUID | None = Field(
        default=None, description='ID категории'
    )
    image_url: AnyUrl | None = Field(
        default=None, description='URL прикрепленного изображения'
    )

    is_published: bool = Field(default=True, description='Опубликовано')


class PostResponseSchema(BaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    text: str = Field(description='Текст')
    pub_date: datetime = Field(description='Дата и время публикации')

    author_id: int = Field(description='ID автора')
    location_id: uuid.UUID | None = Field(
        default=None, description='ID местоположения'
    )
    category_id: uuid.UUID | None = Field(
        default=None, description='ID категории'
    )
    image_url: AnyUrl | None = Field(
        default=None, description='URL прикрепленного изображения'
    )

    is_published: bool = Field(default=True, description='Опубликовано')
    created_at: datetime = Field(description='Дата и время создания')

    model_config = ConfigDict(from_attributes=True)

