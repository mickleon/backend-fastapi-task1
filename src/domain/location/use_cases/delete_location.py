import uuid

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location import LocationRepository


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, id: uuid.UUID):
        with self._database.session() as session:
            self._repo.delete(session=session, id=id)

