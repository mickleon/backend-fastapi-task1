from contextlib import contextmanager
from alembic.config import Config
from alembic import command
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base


class Database:
    def __init__(self) -> None:
        self._db_url = 'sqlite:///sqlite.db'
        self._engine = create_engine(self._db_url)
        self._alembic_cfg = 'alembic.ini'

        @event.listens_for(self._engine, 'connect')
        def _set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute('PRAGMA foreign_keys=ON')
            cursor.close()

    def run_migraions(self) -> None:
        alembic_cfg = Config(self._alembic_cfg)
        command.upgrade(alembic_cfg, 'head')

    @contextmanager
    def session(self):
        connection = self._engine.connect()

        Session = sessionmaker(bind=self._engine)
        session = Session()

        try:
            yield session
            session.commit()
            connection.close()
        except Exception:
            session.rollback()
            raise


database = Database()
Base = declarative_base()
