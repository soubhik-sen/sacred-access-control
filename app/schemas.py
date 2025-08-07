from pydantic import BaseModel
from typing import List, Optional


# ---------- Attribute ----------
class AttributeOut(BaseModel):
    key: str
    value: str

    class Config:
        orm_mode = True


# ---------- Region ----------
class RegionOut(BaseModel):
    region: str

    class Config:
        orm_mode = True


# ---------- Department ----------
class DepartmentOut(BaseModel):
    department: str

    class Config:
        orm_mode = True


# ---------- Role ----------
class RoleOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


# ---------- Permission ----------
class PermissionOut(BaseModel):
    id: int
    action: str
    resource: str

    class Config:
        orm_mode = True


# ---------- User ----------
class UserOut(BaseModel):
    id: int
    username: str
    role: Optional[str]
    clearance_level: Optional[int]
    attributes: List[AttributeOut]
    regions: List[str]
    departments: List[str]

    class Config:
        orm_mode = True


# ---------- Token ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Token Payload ----------
class TokenPayload(BaseModel):
    sub: str
    exp: Optional[int] = None
