from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Boolean

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class MenuItem(Base):

    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )

    item_name: Mapped[str] = mapped_column(
        String(200)
    )

    price: Mapped[float] = mapped_column(
        Numeric(10, 2)
    )

    tax_percentage: Mapped[float] = mapped_column(
        Numeric(5, 2)
    )

    status: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )