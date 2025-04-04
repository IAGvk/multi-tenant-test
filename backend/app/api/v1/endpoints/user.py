from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import CreateUserRequest
from app.models.user import User
from app.db.session import get_db
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/create", response_model=dict)
def create_user(request: CreateUserRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.username == request.user_id,
        User.tenant_id == request.tenant_id
        ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = get_password_hash(request.password)
    new_user = User(
        username=request.user_id,
        tenant_id=request.tenant_id,
        hashed_password=hashed_password
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


from app.pg_db.crud.pg_user import create_pg_user
from app.pg_db.session import get_pg_db

@router.post("/create_pg_user")
def create_pg_user_endpoint(request: CreateUserRequest, db: Session = Depends(get_pg_db)):
    user = create_pg_user(db, request.user_id, request.tenant_id, get_password_hash(request.password))
    return {"message": "User created successfully", "user_id": user.username}