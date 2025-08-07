# app/routers/permissions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.models import Permission
from app.deps import get_db

router = APIRouter(prefix="/permissions", tags=["Permissions"])

# -----------------------------
# Schemas
# -----------------------------

class PermissionCreate(BaseModel):
    name: str

class PermissionOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# -----------------------------
# Routes
# -----------------------------

@router.get("/", response_model=List[PermissionOut])
def list_permissions(db: Session = Depends(get_db)):
    return db.query(Permission).all()


@router.post("/", status_code=201)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    if db.query(Permission).filter(Permission.name == permission.name).first():
        raise HTTPException(status_code=400, detail="Permission already exists")

    new_permission = Permission(name=permission.name)
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return {"id": new_permission.id, "message": "Permission created"}
