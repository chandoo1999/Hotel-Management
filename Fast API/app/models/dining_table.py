from typing import Optional
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class DiningTable(Base):

    __tablename__ = "dining_tables"

    id: Mapped[Optional[int]] = mapped_column(
        primary_key=True,
        nullable=True
    )

    table_number: Mapped[Optional[str]] = mapped_column(
        String(20),
        unique=True,
        nullable=True
    )

    capacity: Mapped[Optional[int]] = mapped_column(
        nullable=True
    )

    is_occupied: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        default=False,
        nullable=True
    )

    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )

    is_active: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        default=True,
        nullable=True
    )