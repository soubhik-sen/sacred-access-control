from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.schemas import UserOut
from app.models import User
from app.utils.rules import user_has_permission

router = APIRouter()


@router.get("/me", response_model=UserOut)
def read_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/check-permission")
def check_permission(
    action: str,
    resource: str,
    current_user: User = Depends(get_current_user),
):
    if user_has_permission(current_user, action, resource):
        return {"allowed": True}
    raise HTTPException(status_code=403, detail="Permission denied")


@router.get("/user-features")
def get_visible_features(current_user: User = Depends(get_current_user)):
    features = []
    for role in current_user.roles:
        for perm in role.permissions:
            features.append(f"{perm.action}:{perm.resource}")
    return {"features": list(set(features))}
