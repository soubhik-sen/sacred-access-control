# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User, Role, UserAttribute
from app.deps import get_db, require_permission
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/users", tags=["Users"])


# -----------------------------
# Pydantic Schemas
# -----------------------------
class RegionCreate(BaseModel):
    region: str

class DepartmentCreate(BaseModel):
    department: str

class AttributeCreate(BaseModel):
    key: str
    value: str

class UserCreate(BaseModel):
    username: str
    password: str  # For now, plain. You’ll hash it later.
    role_id: int
    attributes: Optional[List[AttributeCreate]] = None
    regions: Optional[List[RegionCreate]] = None
    departments: Optional[List[DepartmentCreate]] = None


# -----------------------------
# Routes
# -----------------------------

@router.get("/", response_model=List[dict])
def list_users(db: Session = Depends(get_db),
                user = Depends(require_permission("view"))):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username
            # "role": u.role.name if u.role else None,
            # "attributes": [{ "key": a.key, "value": a.value } for a in u.attributes],
            # "regions": [r.region for r in u.regions],
            # "departments": [d.department for d in u.departments]
        }
        for u in users
    ]


@router.get("/{user_id}", response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.username,
        # "role": user.role.name if user.role else None,
        # "attributes": [{ "key": a.key, "value": a.value } for a in user.attributes]
    }

@router.get("/user_id", response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.username
        # "role": user.role.name if user.role else None,
        # "attributes": [{ "key": a.key, "value": a.value } for a in user.attributes]
    }

@router.post("/", status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    # Check role exists
    role = db.query(Role).filter(Role.id == payload.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role_id")

    user = User(username=payload.username, password=payload.password, role_id=role.id)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Add attributes if any
    if payload.attributes:
        for attr in payload.attributes:
            user_attr = UserAttribute(user_id=user.id, key=attr.key, value=attr.value)
            db.add(user_attr)
        # Regions
    if payload.regions:
        for region in payload.regions:
            db.add(UserRegion(user_id=user.id, region=region.region))

    # Departments
    if payload.departments:
        for dept in payload.departments:
            db.add(UserDepartment(user_id=user.id, department=dept.department))  

    db.commit()

    return {"id": user.id, "message": "User created"}


@router.put("/{user_id}/role")
def update_user_role(user_id: int, new_role_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = db.query(Role).filter(Role.id == new_role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role_id")

    user.role_id = new_role_id
    db.commit()

    return {"message": f"User {user.username} now has role {role.name}"}
