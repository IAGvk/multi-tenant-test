from sqlalchemy.orm import Session
from app.core.config import settings
# from app.db.session import get_db
from app.pg_db.session import get_pg_db
# from app.models.user import User
from app.pg_db.models.pg_user import PGUser
from fastapi import Depends

class DBRouter:
    @staticmethod
    def get_db_session(tenant_name: str) -> Session:
        """Return appropriate database session based on tenant_name"""
        tenant_info = settings.TENANT_MAPPING.get(tenant_name)
        if not tenant_info:
            raise ValueError(f"Unknown tenant: {tenant_name}")
        
        if tenant_info["db_type"] == "postgresql":
            return next(get_pg_db())
        return None

    @staticmethod
    def get_user_model(tenant_name: str):
        """Return appropriate user model based on tenant_name"""
        tenant_info = settings.TENANT_MAPPING.get(tenant_name)
        if not tenant_info:
            raise ValueError(f"Unknown tenant: {tenant_name}")
        
        if tenant_info["db_type"] == "postgresql":
            return PGUser
        return None

    @staticmethod
    def get_tenant_id(tenant_name: str) -> int:
        """Get numeric tenant ID from tenant name"""
        tenant_info = settings.TENANT_MAPPING.get(tenant_name)
        if not tenant_info:
            raise ValueError(f"Unknown tenant: {tenant_name}")
        return tenant_info["id"]


def get_routed_db(tenant_name: str):
    """FastAPI dependency for getting the correct database session"""
    db = DBRouter.get_db_session(tenant_name)
    try:
        yield db
    finally:
        if db:
            db.close()