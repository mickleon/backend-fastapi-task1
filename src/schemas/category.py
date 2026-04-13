from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from src.resources.field_description import (
    TITLE,
    DESCRIPTION,
    IS_PUBLISHED,
    CREATED_AT,
)


class CategoryBaseSchema(BaseModel):
    title: str = Field(max_length=256, description=TITLE)
    description: str = Field(max_length=5000, description=DESCRIPTION)

    is_published: bool = Field(default=True, description=IS_PUBLISHED)


class CategoryRequestSchema(CategoryBaseSchema):
    pass


class CategoryResponseSchema(CategoryBaseSchema):
    created_at: datetime = Field(description=CREATED_AT)

    model_config = ConfigDict(from_attributes=True)
