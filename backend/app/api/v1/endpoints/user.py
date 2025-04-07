from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import CreateUserRequest
from app.core.security import get_password_hash
from app.core.db_router import DBRouter, get_routed_db
from app.pg_db.models.pg_user import PGUser, PGTenant
from app.pg_db.session import get_pg_db

router = APIRouter()

@router.post("/create", response_model=dict)
def create(request: CreateUserRequest):
    """Modified to handle database session based on request body"""
    db = next(get_routed_db(request.tenant_name))  # Get DB session from tenant name in request body
    tenant_id = DBRouter.get_tenant_id(request.tenant_name)
    try:
        # Check if user already exists for this tenant
        existing_user = db.query(PGUser).filter(
            PGUser.username == request.user_id,
            PGUser.tenant_id == tenant_id
        ).first()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create new user
        hashed_password = get_password_hash(request.password)
        new_user = PGUser(
            username=request.user_id,
            tenant_id=tenant_id,
            hashed_password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully"}
    finally:
        db.close()

@router.get("/{user_id}", response_model=dict)
def get_user(user_id: str, db: Session = Depends(get_pg_db)):
    user = db.query(PGUser).filter(PGUser.username == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username, "tenant_id": user.tenant_id}

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: str, db: Session = Depends(get_pg_db)):
    user = db.query(PGUser).filter(PGUser.username == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}