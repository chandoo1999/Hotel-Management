from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.dining_table import DiningTable

# Pydantic schemas
class TableCreate(BaseModel):
    table_number: str
    capacity: int

class TableResponse(TableCreate):
    id: int
    is_occupied: bool
    category_id: Optional[int]
    is_active: bool

    class Config:
        from_attributes = True

# Database methods for create, get (by id, by table_number, by category_id and table_number, all), update, and delete (soft delete) table

def create_table_db(db: Session, table_data: TableCreate, category_id: Optional[int] = None) -> DiningTable:
    """
    Create a new dining table in the database with is_active=True.
    """
    table = DiningTable(
        table_number=table_data.table_number,
        capacity=table_data.capacity,
        is_occupied=False,
        category_id=category_id,
        is_active=True
    )
    db.add(table)
    db.commit()
    db.refresh(table)
    return table

def get_table_by_id(db: Session, table_id: int) -> Optional[DiningTable]:
    """Retrieve a dining table by its unique ID, only if it is active."""
    return db.query(DiningTable).filter(DiningTable.id == table_id, DiningTable.is_active == True).first()

def get_table_by_number(db: Session, table_number: str) -> Optional[List[DiningTable]]:
    """Retrieve tables whose numbers exactly match the given table_number (case-insensitive), only if they are active."""
    return db.query(DiningTable).filter(
        DiningTable.table_number.ilike(table_number),
        DiningTable.is_active == True
    ).all()

def get_table_by_category_and_number(db: Session, category_id: Optional[int], table_number: str) -> Optional[DiningTable]:
    """
    Retrieve a dining table by category_id and table_number, only if it is active.
    If category_id is None, fetch where category_id is NULL.
    """
    query = db.query(DiningTable).filter(
        DiningTable.table_number.ilike(table_number),
        DiningTable.is_active == True,
    )
    if category_id is not None:
        query = query.filter(DiningTable.category_id == category_id)
    else:
        query = query.filter(DiningTable.category_id == None)
    return query.first()

def get_table_by_search_text(db: Session, search_text: str) -> Optional[List[DiningTable]]:
    """Retrieve tables whose table_number contains the search text (case-insensitive), only if they are active."""
    search_pattern = f"%{search_text}%"
    return db.query(DiningTable).filter(
        DiningTable.table_number.ilike(search_pattern),
        DiningTable.is_active == True
    ).all()

def get_all_tables(db: Session) -> List[DiningTable]:
    """Retrieve all active dining tables."""
    return db.query(DiningTable).filter(DiningTable.is_active == True).all()

def update_table_db(db: Session, table: DiningTable, table_data: TableCreate, category_id: Optional[int] = None) -> DiningTable:
    """Update fields of a dining table."""
    table.table_number = table_data.table_number
    table.capacity = table_data.capacity
    if category_id is not None:
        table.category_id = category_id
    db.commit()
    db.refresh(table)
    return table

def delete_table_db(db: Session, table: DiningTable) -> DiningTable:
    """Soft delete a table by setting is_active to False."""
    table.is_active = False
    db.commit()
    db.refresh(table)
    return table