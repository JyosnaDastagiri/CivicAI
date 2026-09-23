"""
SQLAlchemy engine/session setup.

Uses SQLite by default (USE_SQLITE=true) so the project runs with zero
external setup for demo/evaluation purposes. Set USE_SQLITE=false and
provide DATABASE_URL to use PostgreSQL in production.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import get_settings

settings = get_settings()

if settings.USE_SQLITE:
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{settings.SQLITE_PATH}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
