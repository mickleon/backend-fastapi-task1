from src.core.exceptions.database_exceptions import CommentNotFoundException
from src.core.exceptions.domain_exceptions import CommentNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comment import CommentResponseSchema


class GetCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, id: int) -> CommentResponseSchema:
        with self._database.session() as session:
            try:
                comment = self._repo.get(session=session, id=id)
            except CommentNotFoundException:
                raise CommentNotFoundByIdException(id=id)

            return CommentResponseSchema.model_validate(obj=comment)
