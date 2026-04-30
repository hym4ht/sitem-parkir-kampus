from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    # pool_pre_ping=True helps handle connection drops gracefully in MySQL
    pool_pre_ping=True
)

# SessionLocal class will be used as a factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our SQLAlchemy models
Base = declarative_base()

# Dependency to get the DB session from the connection pool
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
