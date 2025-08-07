from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.utils.access import user_has_permission

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
    def permission_dependency(
        user: User = Depends(get_user),
    ):
        if not user_has_permission(user, permission_name):
            raise HTTPException(status_code=403, detail=f"Missing permission: {permission_name}")
        return user
    return permission_dependency