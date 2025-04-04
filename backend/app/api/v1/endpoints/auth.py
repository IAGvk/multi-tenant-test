from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, LoginResponse
from app.models.user import User
from app.core.security import create_access_token, verify_password
from app.db.session import get_db

import bcrypt  # Import bcrypt directly

router = APIRouter()

# Replace pwd_context.verify with bcrypt.checkpw
@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.username == request.user_id,
        User.tenant_id == request.tenant_id
    ).first()
    if not user:
        print("User not found")
        raise HTTPException(status_code=401, detail="Invalid credentials - User Not Found")
    if not verify_password(request.password, user.hashed_password):
        print("Password verification failed")
        raise HTTPException(status_code=401, detail="Invalid credentials - Password Mismatch")
    if user.tenant_id != request.tenant_id:
        raise HTTPException(status_code=403, detail="Access denied for this tenant")
    token = create_access_token(data={"tenant_id": user.tenant_id, "user_id": user.username})
    return LoginResponse(token=token)

from app.pg_db.crud.pg_user import get_pg_user_by_username_and_tenant
from app.pg_db.session import get_pg_db

@router.post("/pg_login", response_model=LoginResponse)
def pg_login(request: LoginRequest, db: Session = Depends(get_pg_db)):
    user = get_pg_user_by_username_and_tenant(db, request.user_id, request.tenant_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials - User Not Found")
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials - Password Mismatch")
    token = create_access_token(data={"tenant_id": user.tenant_id, "user_id": user.username})
    return LoginResponse(token=token)
