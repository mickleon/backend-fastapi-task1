from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Database:
    def __init__(self):
        self._db_url = 'sqlite:///sqlite.db'
        self._engine = create_engine(self._db_url)

    def create_tables(self):
        from src.infrastructure.sqlite.models.user import User
        from src.infrastructure.sqlite.models.category import Category
        from src.infrastructure.sqlite.models.location import Location
        from src.infrastructure.sqlite.models.post import Post
        from src.infrastructure.sqlite.models.comment import Comment

        Base.metadata.create_all(bind=self._engine)

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

