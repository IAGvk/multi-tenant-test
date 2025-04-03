from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, LoginResponse
from app.models.user import User
from app.core.security import create_access_token
from app.db.session import get_db
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.user_id).first()
    if not user or not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.tenant_id != request.tenant_id:
        raise HTTPException(status_code=403, detail="Access denied for this tenant")
    token = create_access_token(data={"tenant_id": user.tenant_id, "user_id": user.username})
    return LoginResponse(token=token)