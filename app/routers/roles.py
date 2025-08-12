# app/routers/roles.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.models import Role, Permission
from app.deps import get_db

router = APIRouter(prefix="/roles", tags=["Roles"])

# -----------------------------
# Schemas
# -----------------------------

class RoleCreate(BaseModel):
    name: str

class PermissionAssign(BaseModel):
    permission_ids: List[int]

class RoleOut(BaseModel):
    id: int
    name: str
    permissions: List[str]

    class Config:
        orm_mode = True


# -----------------------------
# Routes
# -----------------------------

@router.get("/", response_model=List[dict])
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "permissions": [p.name for p in r.permissions]
        }
        for r in roles
    ]


@router.post("/", status_code=201)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    if db.query(Role).filter(Role.name == role.name).first():
        raise HTTPException(status_code=400, detail="Role already exists")

    new_role = Role(name=role.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return {"id": new_role.id, "message": "Role created"}


@router.post("/{role_id}/permissions")
def assign_permissions_to_role(role_id: int, payload: PermissionAssign, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    permissions = db.query(Permission).filter(Permission.id.in_(payload.permission_ids)).all()
    if not permissions:
        raise HTTPException(status_code=400, detail="No valid permissions found")

    role.permissions.extend(p for p in permissions if p not in role.permissions)
    db.commit()

    return {"message": f"Assigned {len(permissions)} permissions to role '{role.name}'"}
