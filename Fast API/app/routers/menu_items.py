from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem
from app.schemas.menu_item import MenuItemCreate
from app.schemas.menu_item import MenuItemResponse
from app.core.database import get_db

router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"]
)


@router.post("/", response_model=MenuItemResponse)
def create_item(
    payload: MenuItemCreate,
    db: Session = Depends(get_db)
):

    item = MenuItem(**payload.model_dump())

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.get("/", response_model=list[MenuItemResponse])
def get_items(
    db: Session = Depends(get_db)
):

    return db.query(MenuItem).all()