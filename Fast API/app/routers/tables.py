from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Union

from app.core.database import get_db
from app.schemas.table import (
    TableCreate,
    TableResponse,
    create_table_db,
    get_table_by_id,
    get_table_by_search_text,
    get_table_by_number,
    get_all_tables,
    update_table_db,
    delete_table_db,
    get_table_by_category_and_number,  # Make sure this is defined in app/schemas/table.py
)
from app.models.dining_table import DiningTable

router = APIRouter(
    prefix="/tables",
    tags=["Tables"]
)

@router.post("/", response_model=TableResponse)
def create_table(
    payload: TableCreate,
    db: Session = Depends(get_db),
    category_id: Optional[int] = Query(None)
):
    # Ensure the table number is unique within the specified category (active tables only)
    existing = get_table_by_category_and_number(db, payload.table_number, category_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A table with this table_number already exists in this category."
        )
    table = create_table_db(db, payload, category_id=category_id)
    return table

@router.get("/", response_model=Union[TableResponse, List[TableResponse]])
def get_tables(
    id: Optional[int] = Query(None),
    search_text: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get all tables or, if 'id' or 'search_text' is specified, return only the matching table(s).
    If input is null, return all tables.
    """
    if id is not None:
        table = get_table_by_id(db, id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")
        return table
    elif search_text is not None:
        tables = get_table_by_search_text(db, search_text)
        if not tables:
            raise HTTPException(status_code=404, detail="No tables found matching search text")
        return tables
    else:
        return get_all_tables(db)

@router.delete("/", response_model=TableResponse)
def delete_table(
    table_id: Optional[int] = Query(None),
    table_number: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Delete (soft) a table by its ID or table_number.
    If both provided, takes ID first.
    """
    table = None
    if table_id is not None:
        table = get_table_by_id(db, table_id)
    elif table_number is not None:
        tables = get_table_by_number(db, table_number)
        if tables:
            table = tables[0]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either table_id or table_number must be provided."
        )
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    deleted_table = delete_table_db(db, table)
    return deleted_table

@router.put("/", response_model=TableResponse)
def update_table(
    table_id: Optional[int] = Query(None),
    table_number: Optional[str] = Query(None),
    payload: TableCreate = None,
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Update a table's fields by id or number (either required).
    """
    if payload is None:
        raise HTTPException(status_code=400, detail="Payload is required.")
    table = None
    if table_id is not None:
        table = get_table_by_id(db, table_id)
    elif table_number is not None:
        tables = get_table_by_number(db, table_number)
        if tables:
            table = tables[0]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either table_id or table_number must be provided."
        )
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    # Prevent duplicate table_number within the specified category (other than itself)
    final_category_id = category_id if category_id is not None else table.category_id
    existing = get_table_by_category_and_number(db, payload.table_number, final_category_id)
    if existing and existing.id != table.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A table with this table_number already exists in this category."
        )
    updated_table = update_table_db(db, table, payload, category_id=category_id)
    return updated_table