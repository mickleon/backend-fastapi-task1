import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.sqlite.database import Base


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, default=uuid.uuid4
    )
    text: Mapped[str] = mapped_column(nullable=False)
    pub_date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    author_id: Mapped[int] = mapped_column(nullable=False)
    location_id: Mapped[uuid.UUID] = mapped_column()
    category_id: Mapped[uuid.UUID] = mapped_column()
    image_ulr: Mapped[str] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    is_published: Mapped[bool] = mapped_column(nullable=False, default=True)

