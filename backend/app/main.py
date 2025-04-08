from fastapi import FastAPI
from app.api.v1.endpoints import user, auth, llm
from app.core.config import settings
from app.core.middleware import TenantMiddleware

# Initialize PostgreSQL database
from app.pg_db.init_pg_db import init_pg_db, init_pg_dummy_data
from app.pg_db.session import PGSessionLocal

init_pg_db()
pg_db = PGSessionLocal()
try:
    init_pg_dummy_data(pg_db)
finally:
    pg_db.close()

# Initialize Qdrant with sample_docs
from app.vector_db.init_qdrant import init_qdrant
init_qdrant()




app = FastAPI(title="Multi-Tenant LLM Backend")

# Add TenantMiddleware
app.add_middleware(TenantMiddleware)

# Include API routers
app.include_router(user.router, prefix="/api/v1/endpoints/user", tags=["User"])
app.include_router(auth.router, prefix="/api/v1/endpoints/auth", tags=["Authentication"])
app.include_router(llm.router, prefix="/api/v1/endpoints/llm", tags=["LLM"])