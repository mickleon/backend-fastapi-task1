from pydantic import BaseModel, Field
from datetime import datetime


SLUG_PATTERN: str = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'


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
