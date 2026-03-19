from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class LocationBaseSchema(BaseModel):
    name: str = Field(max_length=256, description='Название места')
    is_published: bool = Field(default=True, description='Опубликовано')


class LocationRequestSchema(LocationBaseSchema):
    pass


class LocationResponseSchema(LocationBaseSchema):
    created_at: datetime = Field(description='Дата и время создания')

    model_config = ConfigDict(from_attributes=True)
