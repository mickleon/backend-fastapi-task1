import uuid
from pydantic import BaseModel, Field, AnyUrl, ConfigDict
from datetime import datetime


class PostBaseSchema(BaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    text: str = Field(max_length=5000, description='Текст')
    pub_date: datetime = Field(
        default_factory=datetime.now, description='Дата и время публикации'
    )

    author_id: int = Field(description='ID автора')
    location_id: uuid.UUID | None = Field(
        default=None, description='ID местоположения'
    )
    category_id: uuid.UUID | None = Field(
        default=None, description='ID категории'
    )
    image_url: AnyUrl | None = Field(
        default=None, description='URL прикрепленного изображения'
    )

    is_published: bool = Field(default=True, description='Опубликовано')


class PostRequestSchema(PostBaseSchema):
    pass


class PostResponseSchema(PostBaseSchema):
    created_at: datetime = Field(description='Дата и время создания')

    model_config = ConfigDict(from_attributes=True)
