from typing import Optional
from sqlalchemy import String
from sqlalchemy import Boolean

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class Category(Base):

    __tablename__ = "categories"

    id: Mapped[Optional[int]] = mapped_column(
        primary_key=True,
        nullable=True
    )

    category_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True
    )

    is_active: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        default=True,
        nullable=True
    )