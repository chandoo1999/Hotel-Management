from pydantic import BaseModel


class CustomerCreate(BaseModel):
    customer_name: str
    mobile: str
    email: str
    address: str


class CustomerResponse(CustomerCreate):
    id: int

    class Config:
        from_attributes = True  