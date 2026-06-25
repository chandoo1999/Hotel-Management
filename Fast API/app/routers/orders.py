from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.menu_item import MenuItem
from app.models.dining_table import DiningTable

from app.schemas.order import (
    OrderCreate,
    OrderResponse
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/",
    response_model=OrderResponse
)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db)
):

    order = Order(
        # customer_id removed
        table_id=payload.table_id,
        order_type=payload.order_type,
        status="RUNNING"
    )

    db.add(order)

    db.flush()

    total_amount = 0

    for item in payload.items:

        menu_item = db.query(
            MenuItem
        ).filter(
            MenuItem.id == item.item_id
        ).first()

        if not menu_item:
            raise HTTPException(
                404,
                "Menu item not found"
            )

        total = (
            float(menu_item.price)
            * item.quantity
        )

        total_amount += total

        db.add(
            OrderItem(
                order_id=order.id,
                item_id=item.item_id,
                quantity=item.quantity,
                price=menu_item.price,
                total=total
            )
        )

    if payload.table_id:

        table = db.query(
            DiningTable
        ).filter(
            DiningTable.id ==
            payload.table_id
        ).first()

        if table:
            table.is_occupied = True

    db.commit()

    db.refresh(order)

    return order
@router.post("/{order_id}/hold")
def hold_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(Order).get(order_id)

    order.status = "HOLD"

    db.commit()

    return {
        "message": "Order Held"
    }
@router.post("/{order_id}/resume")
def resume_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(Order).get(order_id)

    order.status = "RUNNING"

    db.commit()

    return {
        "message": "Order Resumed"
    }
@router.post("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(Order).get(order_id)

    order.status = "CANCELLED"

    db.commit()

    return {
        "message": "Order Cancelled"
    }
@router.get("/running")
def running_orders(
    db: Session = Depends(get_db)
):

    return db.query(
        Order
    ).filter(
        Order.status == "RUNNING"
    ).all()
