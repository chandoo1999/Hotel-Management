from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import HTTPException
from typing import Optional, List, Union
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse
from app.core.database import get_db
from app.schemas.user import (
    create_user_db,
    get_user_by_id,
    get_user_by_username,
    get_all_users,
    update_user_db,
    delete_user_db,  # Add delete_user_db import
)
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "/",
    response_model=UserResponse
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    # Check each required field separately and raise a separate error for each missing field
    if not payload.username:
        raise HTTPException(
            status_code=422,
            detail="username is required."
        )
    if not payload.name:
        raise HTTPException(
            status_code=422,
            detail="name is required."
        )
    if not payload.role_id:
        raise HTTPException(
            status_code=422,
            detail="role is required."
        )
    if not payload.password:
        raise HTTPException(
            status_code=422,
            detail="password is required."
        )
    # Database activity handled in schemas.user
    user = get_user_by_username(db, payload.username)
    if user is not None:
        raise HTTPException(status_code=404, detail="username already exist")
    user = create_user_db(db, payload)
    return user

@router.get(
    "/",
    response_model=Union[UserResponse, List[UserResponse]]
)
def get_users(
    id: Optional[int] = Query(None),
    username: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get all users or, if 'id' or 'username' is specified, return only the matching user.
    If user input is null, don't return error—just return all users.
    """
    if id is not None:
        user = get_user_by_id(db, id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    elif username is not None:
        user = get_user_by_username(db, username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    else:
        return get_all_users(db)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db)
):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = payload.dict(exclude_unset=True)
    user = update_user_db(db, user, update_data)
    return user

@router.delete(
    "/{user_id}",
    response_model=UserResponse
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = delete_user_db(db, user)
    return user