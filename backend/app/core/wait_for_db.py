import time
import psycopg2
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

def wait_for_db():
    """Wait for database to be ready"""
    max_tries = 60  # Maximum number of attempts
    current_try = 0
    
    while current_try < max_tries:
        try:
            conn = psycopg2.connect(settings.PG_DATABASE_URL)
            conn.close()
            logger.info("Database is ready!")
            return
        except psycopg2.OperationalError as e:
            current_try += 1
            logger.warning(f"Database not ready yet (attempt {current_try}/{max_tries}). Waiting...")
            time.sleep(1)
    
    raise Exception("Could not connect to database within 60 seconds")