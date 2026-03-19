import uuid

from src.core.exceptions.database_exceptions import CategoryNotFoundException
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, id: uuid.UUID):
        with self._database.session() as session:
            try:
                self._repo.delete(session=session, id=id)
            except CategoryNotFoundException:
                raise CategoryNotFoundByIdException(id=id)
