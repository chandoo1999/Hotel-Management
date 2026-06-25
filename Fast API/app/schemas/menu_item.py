from pydantic import BaseModel


class MenuItemCreate(BaseModel):
    category_id: int
    item_name: str
    price: float
    tax_percentage: float


class MenuItemResponse(MenuItemCreate):
    id: int

    class Config:
        from_attributes = True