from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.pg_db.session import PGBase

class PGTenant(PGBase):
    __tablename__ = "pg_tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship("PGUser", back_populates="tenant")

class PGUser(PGBase):
    __tablename__ = "pg_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    tenant_id = Column(Integer, ForeignKey("pg_tenants.id"))

    tenant = relationship("PGTenant", back_populates="users")