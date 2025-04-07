from app.pg_db.session import pg_engine, PGBase
from app.pg_db.models.pg_user import PGUser, PGTenant

def init_pg_db():
    """Initialize PostgreSQL database."""
    print("Initializing PostgreSQL database...")
    print(f"Using database URL: {str(pg_engine.url)}")
    try:
        PGBase.metadata.create_all(bind=pg_engine)
        print("Tables registered:", [table for table in PGBase.metadata.tables.keys()])
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
    print("PostgreSQL database initialized.")

from sqlalchemy.orm import Session
from app.core.security import get_password_hash

def init_pg_dummy_data(db: Session):
    """Initialize PostgreSQL database with dummy tenants and users."""
    print("Creating dummy tenants and users...")
    
    # Create tenants
    tenant_data = [
        {"id": 1, "name": "tenant_1"},
        {"id": 2, "name": "tenant_2"}
    ]
    
    for t_data in tenant_data:
        existing_tenant = db.query(PGTenant).filter(PGTenant.id == t_data["id"]).first()
        if not existing_tenant:
            tenant = PGTenant(**t_data)
            db.add(tenant)
            db.commit()
            print(f"Created tenant: {tenant.name}")
    
    # Create users
    user_data = [
        {
            "username": "ten_1_user_1",
            "tenant_id": 1,
            "password": "ten_1_user_1_pass"
        },
        {
            "username": "ten_2_user_1",
            "tenant_id": 2,
            "password": "ten_2_user_1_pass"
        }
    ]
    
    for u_data in user_data:
        existing_user = db.query(PGUser).filter(PGUser.username == u_data["username"]).first()
        if not existing_user:
            user = PGUser(
                username=u_data["username"],
                tenant_id=u_data["tenant_id"],
                hashed_password=get_password_hash(u_data["password"])
            )
            db.add(user)
            db.commit()
            print(f"Created user: {user.username}")
    
    print("Dummy data initialization completed.")