# app/deps.py

from typing import Optional
from fastapi import Depends, HTTPException, status, Header, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.utils.rules import user_has_permission


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def require_permission(permission_name: str):
    """
    BYPASS AUTH (user-specific):
    - Reads user id from X-User-Id header or ?user_id= query param.
    - Still enforces permission checks for that user.
    - No token/JWT required.
    """
    def permission_dependency(
        db: Session = Depends(get_db),
        x_user_id: Optional[int] = Header(default=None, alias="X-User-Id"),
        q_user_id: Optional[int] = Query(default=None, alias="user_id"),
    ):
        # Prefer header over query param
        user_id = x_user_id if x_user_id is not None else q_user_id
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provide a user id via 'X-User-Id' header or '?user_id=' query param.",
            )

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User id {user_id} not found.",
            )

        if not user_has_permission(user, permission_name, ''):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {permission_name}",
            )
        return user

    return permission_dependency
