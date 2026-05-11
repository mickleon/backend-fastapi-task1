import logging

from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.post import (
    PostRepository,
)
from application.schemas.post import PostResponseSchema

logger = logging.getLogger(__name__)


class GetPostsLastListUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, limit: int) -> list[PostResponseSchema]:
        async with self._database.session() as session:
            posts = await self._repo.get_last_list_published(
                session=session,
                limit=limit,
            )

            return [
                PostResponseSchema.model_validate(obj=post) for post in posts
            ]
