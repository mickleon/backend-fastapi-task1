import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from application.resources.field_description import (
    CREATED_AT,
    IS_PUBLISHED,
    LOCATION_ID,
    LOCATION_NAME,
)


class LocationBaseSchema(BaseModel):
    name: str = Field(max_length=256, description=LOCATION_NAME)


class LocationRequestSchema(LocationBaseSchema):
    pass


class LocationResponseSchema(LocationBaseSchema):
    id: uuid.UUID = Field(description=LOCATION_ID)
    created_at: datetime = Field(description=CREATED_AT)
    is_published: bool = Field(default=True, description=IS_PUBLISHED)

    model_config = ConfigDict(from_attributes=True)
