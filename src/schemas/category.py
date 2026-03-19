from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class CategoryRequestSchema(BaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    description: str = Field(description='Описание')

    is_published: bool = Field(default=True, description='Опубликовано')


class CategoryResponseSchema(BaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    description: str = Field(description='Описание')

    is_published: bool = Field(default=True, description='Опубликовано')
    created_at: datetime = Field(description='Дата и время создания')

    model_config = ConfigDict(from_attributes=True)
