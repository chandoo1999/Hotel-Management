from sqlalchemy.orm import Session

from app.models.user import User

from app.core.security import verify_password
from app.core.security import create_access_token


def authenticate_user(
        db: Session,
        username: str,
        password: str
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        return None

    if not verify_password(
            password,
            user.password_hash
    ):
        return None

    return create_access_token(
        {
            "sub": str(user.id),
            "username": user.username,
            "role_id": user.role_id
        }
    )