from sqlalchemy.orm import Session
from app.models import User, Role, Permission, UserRegion, UserDepartment

def seed_database(db: Session):
    # Create permissions
    p1 = Permission(action="view", resource="orders")
    p2 = Permission(action="edit", resource="orders")
    p3 = Permission(action="view", resource="invoices")


    db.add_all([p1, p2, p3])
    db.commit()

    # Create roles
    admin_role = Role(name="admin", permissions=[p1, p2, p3])
    viewer_role = Role(name="viewer", permissions=[p1, p3])

    db.add_all([admin_role, viewer_role])
    db.commit()

    # Create users
    u1 = User(is_active=True, clearance_level=5)
    u2 = User(is_active=True, clearance_level=2)

    # Assign roles
    u1.roles.append(admin_role)
    u2.roles.append(viewer_role)

    db.add_all([u1, u2])
    db.commit()

    # Add ABAC attributes
    db.add_all([
        UserRegion(user_id=u1.id, region="UK"),
        UserRegion(user_id=u2.id, region="IN"),

        UserDepartment(user_id=u1.id, department="Sales"),
        UserDepartment(user_id=u2.id, department="Logistics"),
    ])
    db.commit()

    print("✅ Seeding complete.")
