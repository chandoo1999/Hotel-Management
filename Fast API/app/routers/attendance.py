from datetime import datetime
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.core.database import get_db

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.post("/checkin")
def checkin(
    employee_id: int,
    db: Session = Depends(get_db)
):

    attendance = Attendance(
        employee_id=employee_id,
        attendance_date=date.today(),
        check_in=datetime.now(),
        status="Present"
    )

    db.add(attendance)
    db.commit()

    return {"message": "Check-in successful"}


@router.post("/checkout")
def checkout(
    attendance_id: int,
    db: Session = Depends(get_db)
):

    attendance = db.query(
        Attendance
    ).filter(
        Attendance.id == attendance_id
    ).first()

    attendance.check_out = datetime.now()

    db.commit()

    return {"message": "Check-out successful"}