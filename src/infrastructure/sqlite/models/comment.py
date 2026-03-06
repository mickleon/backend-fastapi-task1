import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlite.database import Base


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    text: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(nullable=False)
    post_id: Mapped[uuid.UUID] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)

