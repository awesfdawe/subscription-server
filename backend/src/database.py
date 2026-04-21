from sqlmodel import create_engine, Session
from sqlalchemy import event

from src.config import get_settings

settings = get_settings()

echo = False
if settings.environment == "dev":
    echo = True

engine = create_engine(
    settings.database_url,
    echo=echo,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()


def get_session():
    with Session(engine) as session:
        yield session
