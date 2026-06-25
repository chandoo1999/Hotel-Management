from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import Date
from sqlalchemy import Boolean

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class Employee(Base):

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    employee_code: Mapped[str] = mapped_column(
        String(50),
        unique=True
    )

    employee_name: Mapped[str] = mapped_column(
        String(200)
    )

    designation: Mapped[str] = mapped_column(
        String(100)
    )

    department: Mapped[str] = mapped_column(
        String(100)
    )

    salary: Mapped[float] = mapped_column(
        Numeric(12, 2)
    )

    joining_date: Mapped[Date]

    mobile: Mapped[str] = mapped_column(
        String(20)
    )

    status: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )