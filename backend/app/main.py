from fastapi import FastAPI
from app.api.v1.endpoints import user, auth, llm
from app.core.config import settings
from app.core.middleware import TenantMiddleware

####
from app.db.session import engine
from app.db.base import Base

# Initialize the database
Base.metadata.create_all(bind=engine)

#initialise with test users
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
from app.pg_db.init_pg_db import init_pg_db

# Initialize PostgreSQL database
init_pg_db()

# initialize SQLite database
db = SessionLocal()

# Create a test user
test_user = User(
    username="testuser1",
    tenant_id="testtenant1",
    hashed_password=get_password_hash("password123")
)
db.add(test_user)
db.commit()

# Create a test user
test_user = User(
    username="testuser2",
    tenant_id="testtenant2",
    hashed_password=get_password_hash("password123")
)
db.add(test_user)
db.commit()
db.close()
####

app = FastAPI(title="Multi-Tenant LLM Backend")

# Add TenantMiddleware
app.add_middleware(TenantMiddleware)

# Include API routers
app.include_router(user.router, prefix="/api/v1/endpoints/user", tags=["User"])
app.include_router(auth.router, prefix="/api/v1/endpoints/auth", tags=["Authentication"])
app.include_router(llm.router, prefix="/api/v1/endpoints/llm", tags=["LLM"])