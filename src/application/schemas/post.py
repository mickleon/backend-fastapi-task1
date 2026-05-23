import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator

from application.resources.field_description import (
    AUTHOR_ID,
    CATEGORY_ID,
    CREATED_AT,
    HAS_NEXT,
    IMAGE_IDS,
    IMAGES,
    IS_PUBLISHED,
    LOCATION_ID,
    POST_ID,
    POST_LIST_ITEMS,
    PUB_DATE,
    TEXT,
    TITLE,
)
from application.schemas.image import ImageResponseSchema


class PostBaseSchema(BaseModel):
    title: str = Field(max_length=256, description=TITLE)
    text: str = Field(max_length=5000, description=TEXT)

    location_id: uuid.UUID | None = Field(default=None, description=LOCATION_ID)
    category_id: uuid.UUID = Field(description=CATEGORY_ID)


class PostImageIdsMixin(BaseModel):
    image_ids: list[uuid.UUID] = Field(
        default_factory=list, description=IMAGE_IDS
    )


class PostRequestSchema(PostBaseSchema, PostImageIdsMixin):
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


class PostUpdateSchema(PostBaseSchema, PostImageIdsMixin):
    pass


class PostUpdateAdminSchema(PostBaseSchema, PostImageIdsMixin):
    is_published: bool = Field(default=True, description=IS_PUBLISHED)
    pub_date: datetime = Field(description=PUB_DATE)


class PostResponseSchema(PostBaseSchema):
    id: uuid.UUID = Field(description=POST_ID)
    author_id: int = Field(description=AUTHOR_ID)
    created_at: datetime = Field(description=CREATED_AT)
    pub_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description=PUB_DATE,
    )
    is_published: bool = Field(default=True, description=IS_PUBLISHED)
    images: list[ImageResponseSchema] = Field(
        default_factory=list, description=IMAGES
    )

    model_config = ConfigDict(from_attributes=True)


class PostsPageResponseSchema(BaseModel):
    items: list[PostResponseSchema] = Field(
        default_factory=list, description=POST_LIST_ITEMS
    )
    has_next: bool = Field(description=HAS_NEXT)
