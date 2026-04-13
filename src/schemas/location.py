from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from src.resources.field_description import (
    CREATED_AT,
    IS_PUBLISHED,
    LOCATION_NAME,
)


class LocationBaseSchema(BaseModel):
    name: str = Field(max_length=256, description=LOCATION_NAME)
    is_published: bool = Field(default=True, description=IS_PUBLISHED)


class LocationRequestSchema(LocationBaseSchema):
    pass


class LocationResponseSchema(LocationBaseSchema):
    created_at: datetime = Field(description=CREATED_AT)

    model_config = ConfigDict(from_attributes=True)
