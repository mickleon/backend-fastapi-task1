from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class CategoryBaseSchema(BaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    description: str = Field(max_length=5000, description='Описание')

    is_published: bool = Field(default=True, description='Опубликовано')


class CategoryRequestSchema(CategoryBaseSchema):
    pass


class CategoryResponseSchema(CategoryBaseSchema):
    created_at: datetime = Field(description='Дата и время создания')

    model_config = ConfigDict(from_attributes=True)
