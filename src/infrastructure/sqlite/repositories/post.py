import uuid
from typing import Type
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from src.infrastructure.sqlite.models.post import Post as PostModel
from src.infrastructure.sqlite.models.user import User as UserModel
from src.infrastructure.sqlite.models.location import Location as LocationModel
from src.infrastructure.sqlite.models.category import Category as CategoryModel
from src.schemas.post import PostRequestSchema


class PostRepository:
    def __init__(self) -> None:
        self._model: Type[PostModel] = PostModel
        self._author_model: Type[UserModel] = UserModel
        self._location_model: Type[LocationModel] = LocationModel
        self._category_model: Type[CategoryModel] = CategoryModel

    def get(self, session: Session, id: uuid.UUID) -> PostModel:
        query = select(self._model).where(self._model.id == id)
        post = session.scalar(query)

        if not post:
            raise PostNotFoundException()

        return post

    def create(self, session: Session, data: PostRequestSchema) -> PostModel:
        author = session.get(self._author_model, data.author_id)
        if not author:
            raise UserNotFoundException()

        if data.location_id is not None:
            location = session.get(self._location_model, data.location_id)
            if not location:
                raise LocationNotFoundException()

        if data.category_id is not None:
            category = session.get(self._category_model, data.category_id)
            if not category:
                raise CategoryNotFoundException()

        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        post = session.scalar(query)

        return post

    def update(
        self, session: Session, id: uuid.UUID, data: PostRequestSchema
    ) -> PostModel:
        post = session.get(self._model, id)
        if not post:
            raise PostNotFoundException()

        update_data = data.model_dump(exclude_unset=True)

        if (
            'author_id' in update_data
            and update_data['author_id'] != post.author_id
        ):
            author = session.get(self._author_model, update_data['author_id'])
            if not author:
                raise UserNotFoundException()

        if (
            'location_id' in update_data
            and update_data['location_id'] is not None
            and update_data['location_id'] != post.location_id
        ):
            location = session.get(
                self._location_model, update_data['location_id']
            )
            if not location:
                raise LocationNotFoundException()

        if (
            'category_id' in update_data
            and update_data['category_id'] is not None
            and update_data['category_id'] != post.category_id
        ):
            category = session.get(
                self._category_model, update_data['category_id']
            )
            if not category:
                raise CategoryNotFoundException()

        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(**update_data)
            .returning(self._model)
        )
        post = session.scalar(query)

        return post

    def delete(self, session: Session, id: uuid.UUID) -> None:
        query = delete(self._model).where(self._model.id == id)
        result = session.execute(query)

        if not result.rowcount:
            raise PostNotFoundException()
