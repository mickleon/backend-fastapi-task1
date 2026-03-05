from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.comment import Comment
from src.infrastructure.sqlite.repositories.comment import CommentRepository
from src.schemas.comment import CommentRequestSchema, CommentResponseSchema


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, data: CommentRequestSchema):
        with self._database.session() as session:
            comment = Comment(**data.model_dump())
            self._repo.create(session=session, comment=comment)

        return CommentResponseSchema.model_validate(obj=comment)

