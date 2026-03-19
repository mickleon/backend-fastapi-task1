from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comment import CommentRepository


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, id: int):
        with self._database.session() as session:
            self._repo.delete(session=session, id=id)

