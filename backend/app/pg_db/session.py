from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# PostgreSQL connection URL from environment variables
PG_DATABASE_URL = os.getenv("PG_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/multi_tenant_pg_db")

pg_engine = create_engine(PG_DATABASE_URL)
PGSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pg_engine)
PGBase = declarative_base()

def get_pg_db():
    """Dependency to get a PostgreSQL database session."""
    db = PGSessionLocal()
    try:
        yield db
    finally:
        db.close()