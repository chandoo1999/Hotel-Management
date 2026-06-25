from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from app.schemas.customer import CustomerResponse
from app.core.database import get_db

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post("/", response_model=CustomerResponse)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db)
):

    customer = Customer(**payload.model_dump())

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@router.get("/", response_model=list[CustomerResponse])
def get_customers(
    db: Session = Depends(get_db)
):

    return db.query(Customer).all()