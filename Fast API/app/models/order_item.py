from sqlalchemy import ForeignKey
from sqlalchemy import Numeric

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


class OrderItem(Base):

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )

    item_id: Mapped[int] = mapped_column(
        ForeignKey("menu_items.id")
    )

    quantity: Mapped[int]

    price: Mapped[float] = mapped_column(
        Numeric(10, 2)
    )

    total: Mapped[float] = mapped_column(
        Numeric(10, 2)
    )

    order = relationship(
        "Order",
        back_populates="items"
    )