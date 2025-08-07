from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, models
from app.security import oauth2_scheme


# Replace with your actual secret and algorithm
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = crud.get_user_with_roles_permissions(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive or missing user")

    return user
