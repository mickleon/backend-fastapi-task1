import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from application.resources.field_description import CREATED_AT, IMAGE_ID


class ImageResponseSchema(BaseModel):
    id: uuid.UUID = Field(description=IMAGE_ID)
    created_at: datetime = Field(description=CREATED_AT)

    model_config = ConfigDict(from_attributes=True)


class ImageUploadResponseSchema(BaseModel):
    id: uuid.UUID = Field(description=IMAGE_ID)
