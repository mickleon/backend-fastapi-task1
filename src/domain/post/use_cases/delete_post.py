import uuid

from src.core.exceptions.database_exceptions import PostNotFoundException
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, id: uuid.UUID):
        with self._database.session() as session:
            try:
                self._repo.delete(session=session, id=id)
            except PostNotFoundException:
                raise PostNotFoundByIdException(id=id)
