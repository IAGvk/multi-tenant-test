from sqlalchemy.orm import Session
from app.pg_db.models.pg_user import PGUser
from app.schemas.auth import LoginRequest

def get_pg_user_by_username_and_tenant(db: Session, username: str, tenant_id: int):
    return db.query(PGUser).filter(PGUser.username == username, PGUser.tenant_id == tenant_id).first()

def create_pg_user(db: Session, username: str, tenant_id: int, hashed_password: str):
    user = PGUser(username=username, tenant_id=tenant_id, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user