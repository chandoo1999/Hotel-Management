from datetime import datetime

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("customers.id"),
        nullable=True
    )

    table_id: Mapped[int | None] = mapped_column(
        ForeignKey("dining_tables.id"),
        nullable=True
    )

    order_type: Mapped[str] = mapped_column(
        String(20)
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="RUNNING"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete"
    )