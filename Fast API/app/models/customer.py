from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class Customer(Base):

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    customer_name: Mapped[str] = mapped_column(
        String(200)
    )

    mobile: Mapped[str] = mapped_column(
        String(20)
    )

    email: Mapped[str] = mapped_column(
        String(150)
    )

    address: Mapped[str] = mapped_column(
        Text
    )