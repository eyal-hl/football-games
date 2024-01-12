from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from backend.config import config

# create session factory to generate new database sessions
SessionFactory = async_sessionmaker(
    bind=create_async_engine(config.database.dsn),
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def create_session() -> Iterator[Session]:
    """Create new database session.

    Yields:
        Database session.
    """

    session = SessionFactory()

    try:
        yield session
        await session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        await session.close()


@contextmanager
def open_session() -> Iterator[Session]:
    """Create new database session with context manager.

    Yields:
        Database session.
    """

    return create_session()
