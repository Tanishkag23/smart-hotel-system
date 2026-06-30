from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Abhi ke liye SQLite use karenge (simple file-based DB, dev ke liye perfect)
SQLALCHEMY_DATABASE_URL = "sqlite:///./hotel.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency function - har API request ko ek database session milega
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()