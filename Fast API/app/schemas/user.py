from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.core.security import hash_password
from fastapi import HTTPException

# Pydantic schemas
class UserCreate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    role_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    role_id: Optional[int] = None

    class Config:
        from_attributes = True

# Database activity methods for create, update, get, and soft-delete operations on users

def create_user_db(db: Session, user_data: UserCreate) -> User:
    """
    Create a new user in the database with is_active=True (active).
    If a user with the same username already exists, raise HTTP 400 error.
    """
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="A user with this username already exists.")
    user = User(
        username=user_data.username,
        name=user_data.name,
        password_hash=hash_password(user_data.password),
        email=user_data.email,
        mobile=user_data.mobile,
        role_id=user_data.role_id,
        is_active=True  # Soft delete field: active on create
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Just in case unique constraint is violated not caught by previous query
        raise HTTPException(status_code=400, detail="A user with this username already exists.")
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Retrieve a user by their unique ID (only active users)."""
    return db.query(User).filter(User.id == user_id, User.is_active == True).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Retrieve a user by their unique username (only active users)."""
    return db.query(User).filter(User.username == username, User.is_active == True).first()

def get_all_users(db: Session) -> List[User]:
    """Retrieve all active users from the database."""
    return db.query(User).filter(User.is_active == True).all()

def update_user_db(db: Session, user: User, update_data: dict) -> User:
    """Update user attributes in the database."""
    for key, value in update_data.items():
        if hasattr(user, key) and value is not None:
            # Map 'password' to 'password_hash'
            if key == "password":
                setattr(user, "password_hash", hash_password(value))
            else:
                setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user_db(db: Session, user: User) -> User:
    """Soft delete a user by setting is_active to False (inactive)."""
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user