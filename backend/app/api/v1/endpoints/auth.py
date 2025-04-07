from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, LoginResponse
from app.core.security import create_access_token, verify_password
from app.core.db_router import DBRouter, get_routed_db
from app.core.config import settings  # Add this import


router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    """Modified to handle database session based on request body"""
    db = next(get_routed_db(request.tenant_name))  # Get DB session from tenant name in request body
    try:
        tenant_id = DBRouter.get_tenant_id(request.tenant_name)  # Convert name to ID
        UserModel = DBRouter.get_user_model(request.tenant_name)
        
        user = db.query(UserModel).filter(
            UserModel.username == request.user_id,
            UserModel.tenant_id == tenant_id
        ).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials - User Not Found")
        if not verify_password(request.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials - Password Mismatch")
        
        token = create_access_token(data={
            "tenant_id": tenant_id,  # Use converted ID
            "tenant_name": request.tenant_name,
            "user_id": user.username,
            "db_type": settings.TENANT_MAPPING[request.tenant_name]["db_type"]
        })
        return LoginResponse(token=token)
    finally:
        db.close()
