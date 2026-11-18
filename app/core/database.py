# Package	Why we need it
# SQLAlchemy -	Communicates with PostgreSQL using Python
# Alembic -	Creates and manages database migrations
# psycopg -	PostgreSQL database driver
# python-dotenv	- Reads database configuration from .env


import os
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Load database configuration from the project's .env file.
load_dotenv()

# Read the database connection URL from the environment.
DATABASE_URL = os.getenv("DATABASE_URL")

# Stop early with a clear error if the URL is missing.
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured in the .env file")

# Create the SQLAlchemy engine.
# pool_pre_ping checks that a database connection is still alive.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Create database sessions for individual API requests.
# autoflush=False gives us explicit control over when changes are sent.
# autocommit=False means transactions must be committed explicitly.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Base class for all SQLAlchemy database models.
class Base(DeclarativeBase):
    pass


# FastAPI dependency: provide a database session and always close it.
# If a database operation fails during an API request, we can capture the exception and its traceback.
logger = logging.getLogger("eaiirp")

def get_db():
    db = SessionLocal()

    try:
        yield db

    except Exception:
        # Record database-related errors with traceback.
        logger.exception("Database session error")
        raise

    finally:
        # Always release the database connection.
        db.close()
