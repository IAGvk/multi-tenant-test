from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest
from app.models.user import User
from app.db.session import get_db
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create a new user
@router.post("/create", response_model=dict)
def create_user(request: LoginRequest, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.username == request.user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash the password and create the user
    hashed_password = pwd_context.hash(request.password)
    new_user = User(
        username=request.user_id,
        hashed_password=hashed_password,
        tenant_id=request.tenant_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

# Get user details
@router.get("/{user_id}", response_model=dict)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username, "tenant_id": user.tenant_id}

# Delete a user
@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}