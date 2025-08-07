# app/utils/rules.py

from app.models import User
from typing import List


def user_has_permission(user: User, action: str, resource: str) -> bool:
    return any(
        perm.action == action and perm.resource == resource
        for role in user.roles
        for perm in role.permissions
    )



def user_has_all_permissions(user: User, required: List[tuple]) -> bool:
    """
    required: list of (action, resource) tuples
    """
    user_perms = {
        (perm.action, perm.resource)
        for role in user.roles
        for perm in role.permissions
    }
    return all((a, r) in user_perms for (a, r) in required)
