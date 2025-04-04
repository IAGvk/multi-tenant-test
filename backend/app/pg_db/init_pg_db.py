from app.pg_db.session import pg_engine, PGBase
from app.pg_db.models.pg_user import PGUser, PGTenant

def init_pg_db():
    """Initialize PostgreSQL database."""
    print("Initializing PostgreSQL database...")
    PGBase.metadata.create_all(bind=pg_engine)
    print("PostgreSQL database initialized.")