"""Database helpers (SQLAlchemy) for the Sisloterias project."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sisloterias.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that provides a database session.

    Yields:
        sqlalchemy.orm.Session: a database session.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
