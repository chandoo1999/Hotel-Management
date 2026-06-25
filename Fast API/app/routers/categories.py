from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Union

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from app.core.database import get_db
from app.schemas.category import (
    create_category_db,
    get_category_by_id,
    get_all_categories,
    delete_category_db,
    get_category_by_name,
    get_category_by_search_text,
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/", response_model=CategoryResponse)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db)
):
    # Prevent duplicate category names (only active categories matter)
    existing = get_category_by_name(db, payload.category_name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A category with this name already exists."
        )
    category = create_category_db(db, payload)
    return category

@router.get(
    "/", 
    response_model=Union[CategoryResponse, List[CategoryResponse]]
)
def get_categories(
    id: Optional[int] = Query(None),
    search_text: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get all categories or, if 'id' or 'category_name' is specified, return only the matching category.
    If input is null, return all categories.
    """
    if id is not None:
        category = get_category_by_id(db, id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    elif search_text is not None:
        category = get_category_by_search_text(db, search_text)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    else:
        return get_all_categories(db)

@router.delete("/", response_model=CategoryResponse)
def delete_category(
    category_id: Optional[int] = Query(None),
    category_name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Delete a category either by its ID or by its name.
    - If both are provided, will try by ID first.
    - If neither is given, throw error.
    """
    if category_id is not None:
        # Delete by ID
        category = get_category_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        deleted_category = delete_category_db(db, category)
        return deleted_category
    elif category_name is not None:
        # Find active category with exact name
        categories = get_category_by_name(db, category_name)
        if not categories or len(categories) == 0:
            raise HTTPException(status_code=404, detail="Category not found")
        # If more than one (shouldn't happen if unique=True), but we handle it anyway by picking the first
        category = categories[0]
        deleted_category = delete_category_db(db, category)
        return deleted_category
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either category_id or category_name must be provided."
        )

@router.put("/", response_model=CategoryResponse)
def update_category(
    category_id: Optional[int] = Query(None),
    category_name: Optional[str] = Query(None),
    payload: CategoryCreate = None,
    db: Session = Depends(get_db)
):
    """
    Update a category's name by category_id or category_name (either required).
    """
    if not payload:
        raise HTTPException(status_code=400, detail="Payload is required.")
    category = None

    if category_id is not None:
        category = get_category_by_id(db, category_id)
    elif category_name is not None:
        # Find active category with exact (case-insensitive) name
        categories = get_category_by_name(db, category_name)
        if categories and len(categories) > 0:
            category = categories[0]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either category_id or category_name must be provided."
        )
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Prevent duplicate category names (other than itself)
    existing = db.query(Category).filter(
        Category.category_name == payload.category_name,
        Category.id != category.id,
        Category.is_active == True
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A category with this name already exists."
        )
    category.category_name = payload.category_name
    db.commit()
    db.refresh(category)
    return category