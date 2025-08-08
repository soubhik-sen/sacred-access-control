# app/models.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

# Association table between roles and permissions
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True)
)
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True)
)
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    action = Column(String, nullable=False)    # e.g., "view", "edit"
    resource = Column(String, nullable=False)  # e.g., "order", "invoice"

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")


class UserRegion(Base):
    __tablename__ = "user_regions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    region = Column(String)

    user = relationship("User", back_populates="regions")


class UserDepartment(Base):
    __tablename__ = "user_departments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    department = Column(String)

    user = relationship("User", back_populates="departments")


# Add these to User class:
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    clearance_level = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    roles = relationship("Role", secondary=user_roles, back_populates="users")

    attributes = relationship("UserAttribute", back_populates="user")

    # Add these:
    regions = relationship("UserRegion", back_populates="user")
    departments = relationship("UserDepartment", back_populates="user")


class UserAttribute(Base):
    __tablename__ = "user_attributes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key = Column(String)   # e.g., 'region', 'department'
    value = Column(String) # e.g., 'East', 'HR'

    user = relationship("User", back_populates="attributes")
