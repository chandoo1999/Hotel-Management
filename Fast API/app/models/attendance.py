from sqlalchemy import ForeignKey
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class Attendance(Base):

    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id")
    )

    attendance_date: Mapped[Date]

    check_in: Mapped[DateTime]

    check_out: Mapped[DateTime]

    status: Mapped[str] = mapped_column(
        String(20)
    )