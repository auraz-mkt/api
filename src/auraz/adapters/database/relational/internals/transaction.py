from functools import wraps
from typing import Any, Callable

from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker


def _get_session_or_create(engine: Engine, **kwargs) -> Session:
    existing_session = kwargs.get("session")
    create_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return existing_session or create_session()


def transaction(func) -> Callable[..., Any]:
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        session = _get_session_or_create(self.engine, **kwargs)
        try:
            result = await func(session, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return wrapper
