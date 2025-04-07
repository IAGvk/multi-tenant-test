from sqlalchemy.orm import Session
from app.pg_db.models.pg_user import PGUser
from app.schemas.auth import LoginRequest
from fastapi import APIRouter, Depends, HTTPException

from app.core.db_router import DBRouter, get_routed_db 

def get_pg_user_by_username_and_tenant(username: str, tenant_id: int, db: Session = Depends(get_routed_db)):
    return db.query(PGUser).filter(PGUser.username == username, PGUser.tenant_id == tenant_id).first()

def create_pg_user(username: str, tenant_name: str, hashed_password: str, db: Session = Depends(get_routed_db)):
    tenant_id = DBRouter.get_tenant_id(tenant_name)
    user = PGUser(username=username, tenant_id=tenant_id, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user