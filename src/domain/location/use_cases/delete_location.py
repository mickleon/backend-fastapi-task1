import uuid

from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location import LocationRepository


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, id: uuid.UUID) -> None:
        with self._database.session() as session:
            try:
                self._repo.delete(session=session, id=id)
            except LocationNotFoundException:
                raise LocationNotFoundByIdException(id=id)
