import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from pydantic import AnyUrl, BaseModel, ConfigDict, Field, field_validator

from application.resources.field_description import (
    AUTHOR_ID,
    CATEGORY_ID,
    CREATED_AT,
    HAS_NEXT,
    IMAGE_URL,
    IS_PUBLISHED,
    LOCATION_ID,
    POST_ID,
    POST_LIST_ITEMS,
    PUB_DATE,
    TEXT,
    TITLE,
)


class PostBaseSchema(BaseModel):
    title: str = Field(max_length=256, description=TITLE)
    text: str = Field(max_length=5000, description=TEXT)

    location_id: uuid.UUID | None = Field(default=None, description=LOCATION_ID)
    category_id: uuid.UUID | None = Field(default=None, description=CATEGORY_ID)
    image_url: AnyUrl | None = Field(default=None, description=IMAGE_URL)


class PostRequestSchema(PostBaseSchema):
    pub_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description=PUB_DATE,
    )

    @field_validator('pub_date', mode='after')
    @staticmethod
    def check_pub_date(pub_date: datetime) -> datetime:
        if pub_date < datetime.now(timezone.utc) - timedelta(seconds=5):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Нельзя делать публикации с прошедшей датой публикации',
            )
        return pub_date


class PostRequestAdminSchema(PostRequestSchema):
    is_published: bool = Field(default=True, description=IS_PUBLISHED)


class PostUpdateSchema(PostBaseSchema):
    pass


class PostUpdateAdminSchema(PostBaseSchema):
    is_published: bool = Field(default=True, description=IS_PUBLISHED)


class PostResponseSchema(PostBaseSchema):
    id: uuid.UUID = Field(description=POST_ID)
    author_id: int = Field(description=AUTHOR_ID)
    created_at: datetime = Field(description=CREATED_AT)
    is_published: bool = Field(default=True, description=IS_PUBLISHED)

    model_config = ConfigDict(from_attributes=True)


class PostsPageResponseSchema(BaseModel):
    items: list[PostResponseSchema] = Field(
        default_factory=list, description=POST_LIST_ITEMS
    )
    has_next: bool = Field(description=HAS_NEXT)
