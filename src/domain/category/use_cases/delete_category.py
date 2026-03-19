import uuid

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, id: uuid.UUID):
        with self._database.session() as session:
            self._repo.delete(session=session, id=id)

