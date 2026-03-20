from src.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    UserNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    UserNotFoundByIdException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.post import PostRequestSchema, PostResponseSchema


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, data: PostRequestSchema) -> PostResponseSchema:
        with self._database.session() as session:
            try:
                post = self._repo.create(session=session, data=data)
            except UserNotFoundException:
                raise UserNotFoundByIdException(id=data.author_id)
            except CategoryNotFoundException:
                if data.category_id is not None:
                    raise CategoryNotFoundByIdException(id=data.category_id)
                raise CategoryNotFoundException()
            except LocationNotFoundException:
                if data.location_id is not None:
                    raise LocationNotFoundByIdException(id=data.location_id)
                raise LocationNotFoundException()

            return PostResponseSchema.model_validate(obj=post)
