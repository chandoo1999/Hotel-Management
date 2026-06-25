from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from sqlalchemy import String

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[Optional[int]] = mapped_column(
        primary_key=True,
        index=True,
        nullable=True
    )

    username: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        nullable=True
    )

    name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True
    )

    mobile: Mapped[Optional[str]] = mapped_column(
        String(20),
        unique=True,
        nullable=True
    )

    password_hash: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    is_active: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        default=True,
        nullable=True
    )

    role_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("roles.id"),
        nullable=True
    )

    role = relationship("Role")