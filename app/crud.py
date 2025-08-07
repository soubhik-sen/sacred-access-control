from sqlalchemy.orm import Session
from app import models


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_with_roles_permissions(db: Session, user_id: int) -> models.User:
    return (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .options(
            # Eager-load relationships to avoid lazy loading issues
            models.joinedload(models.User.roles).joinedload(models.Role.permissions),
            models.joinedload(models.User.regions),
            models.joinedload(models.User.departments),
            models.joinedload(models.User.attributes)
        )
        .first()
    )
