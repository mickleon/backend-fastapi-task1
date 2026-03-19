from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comment import CommentResponseSchema


class GetCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, id: int) -> CommentResponseSchema:
        with self._database.session() as session:
            comment = self._repo.get(session=session, id=id)
            return CommentResponseSchema.model_validate(obj=comment)

