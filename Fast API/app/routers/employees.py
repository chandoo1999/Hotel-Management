from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate
from app.schemas.employee import EmployeeResponse
from app.core.database import get_db

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post("/", response_model=EmployeeResponse)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db)
):

    employee = Employee(**payload.model_dump())

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


@router.get("/", response_model=list[EmployeeResponse])
def get_employees(
    db: Session = Depends(get_db)
):

    return db.query(Employee).all()