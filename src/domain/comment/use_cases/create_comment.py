from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comment import CommentRequestSchema, CommentResponseSchema


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, data: CommentRequestSchema):
        with self._database.session() as session:
            comment = self._repo.create(session=session, data=data)

            return CommentResponseSchema.model_validate(obj=comment)

