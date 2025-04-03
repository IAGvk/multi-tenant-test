from fastapi import FastAPI
from app.api.v1.endpoints import user, auth, llm
from app.core.config import settings
from app.core.middleware import TenantMiddleware

app = FastAPI(title="Multi-Tenant LLM Backend")

# Add TenantMiddleware
app.add_middleware(TenantMiddleware)

# Include API routers
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(llm.router, prefix="/api/v1/llm", tags=["LLM"])