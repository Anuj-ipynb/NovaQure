from collections.abc import Generator

from sqlalchemy.orm import Session

from backend.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Creates a new database session for every request.

    The session is automatically closed
    after the request finishes.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
