from pydantic import BaseModel
from datetime import date


class EmployeeCreate(BaseModel):
    employee_code: str
    employee_name: str
    designation: str
    department: str
    salary: float
    joining_date: date
    mobile: str


class EmployeeResponse(EmployeeCreate):
    id: int

    class Config:
        from_attributes = True