from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.category import Category

# Pydantic schemas
class CategoryCreate(BaseModel):
    category_name: str

class CategoryResponse(CategoryCreate):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# Database methods for create, get (by id, by name, all), and delete (soft delete) category

def create_category_db(db: Session, category_data: CategoryCreate) -> Category:
    """
    Create a new category in the database with is_active=True.
    """
    category = Category(
        category_name=category_data.category_name,
        is_active=True
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_category_by_id(db: Session, category_id: int) -> Optional[Category]:
    """Retrieve a category by its unique ID, only if it is active."""
    return db.query(Category).filter(Category.id == category_id, Category.is_active == True).first()

def get_category_by_name(db: Session, category_name: str) -> Optional[List[Category]]:
    """Retrieve categories whose names exactly match the given name (case-insensitive), only if they are active."""
    return db.query(Category).filter(
        Category.category_name.ilike(category_name),
        Category.is_active == True
    ).all()
    
def get_category_by_search_text(db: Session, search_text: str) -> Optional[List[Category]]:
    """Retrieve categories whose names contain the search text (case-insensitive), only if they are active."""
    search_pattern = f"%{search_text}%"
    return db.query(Category).filter(
        Category.category_name.ilike(search_pattern),
        Category.is_active == True
    ).all()

def get_all_categories(db: Session) -> List[Category]:
    """Retrieve all active categories."""
    return db.query(Category).filter(Category.is_active == True).all()

def delete_category_db(db: Session, category: Category) -> Category:
    """Soft delete a category by setting is_active to False."""
    category.is_active = False
    db.commit()
    db.refresh(category)
    return category
   