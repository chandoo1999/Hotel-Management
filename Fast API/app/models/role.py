from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import String

from app.core.database import Base


class Role(Base):

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    role_name: Mapped[str] = mapped_column(
        String(50),
        unique=True
    )