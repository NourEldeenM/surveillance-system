from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import DATABASE

DATABASE_URL = DATABASE.DATABASE_URL


if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file!")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()