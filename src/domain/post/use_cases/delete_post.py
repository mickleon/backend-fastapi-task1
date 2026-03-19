import uuid

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, id: uuid.UUID):
        with self._database.session() as session:
            self._repo.delete(session=session, id=id)

