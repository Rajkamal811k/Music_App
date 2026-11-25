import ssl
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.core.config import settings
from app.database.connection import Base

# Import all models so Alembic can detect them
from app.models import User, CreatorProfile


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

db_url = settings.DATABASE_URL
connect_args = {}
if db_url.startswith("postgresql://") or db_url.startswith("postgres://"):
    base_url = db_url.split("?")[0]
    db_url = base_url.replace("postgresql://", "postgresql+pg8000://").replace("postgres://", "postgresql+pg8000://")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connect_args["ssl_context"] = ctx

config.set_main_option(
    "sqlalchemy.url",
    db_url.replace("%", "%%")
)

target_metadata = Base.metadata


def run_migrations_offline():
    url = db_url

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=connect_args
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
