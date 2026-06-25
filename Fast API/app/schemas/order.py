from pydantic import BaseModel


class OrderItemCreate(BaseModel):

    item_id: int
    quantity: int


class OrderCreate(BaseModel):

    customer_id: int | None = None

    table_id: int | None = None

    order_type: str

    items: list[OrderItemCreate]


class OrderResponse(BaseModel):

    id: int

    status: str

    order_type: str

    class Config:
        from_attributes = True