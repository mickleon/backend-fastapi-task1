from src.core.exceptions.database_exceptions import (
    PostNotFoundException,
    UserNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comment import CommentRequestSchema, CommentResponseSchema


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, data: CommentRequestSchema):
        with self._database.session() as session:
            try:
                comment = self._repo.create(session=session, data=data)
            except PostNotFoundException:
                raise PostNotFoundByIdException(id=data.post_id)
            except UserNotFoundException:
                raise UserNotFoundByIdException(id=data.author_id)

            return CommentResponseSchema.model_validate(obj=comment)
