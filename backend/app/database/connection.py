import ssl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings

db_url = settings.DATABASE_URL
connect_args = {}

# Use pure-Python pg8000 driver to bypass Windows Application Control blocking binary DLLs
if db_url.startswith("postgresql://") or db_url.startswith("postgres://"):
    base_url = db_url.split("?")[0]
    db_url = base_url.replace("postgresql://", "postgresql+pg8000://").replace("postgres://", "postgresql+pg8000://")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connect_args["ssl_context"] = ctx

engine = create_engine(
    db_url,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
