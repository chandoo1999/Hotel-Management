from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest
from app.schemas.auth import TokenResponse

from app.services.auth_service import authenticate_user

from app.core.database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
        payload: LoginRequest,
        db: Session = Depends(get_db)
):

    token = authenticate_user(
        db,
        payload.username,
        payload.password
    )

    if not token:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "access_token": token
    }