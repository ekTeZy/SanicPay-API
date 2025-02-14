from logging.config import fileConfig
import os
from sqlalchemy import create_engine, pool
from alembic import context
from app.db.models import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


sync_engine = create_engine(
    os.getenv("DATABASE_URL").replace("postgresql+asyncpg", "postgresql"),
    poolclass=pool.NullPool
)

def run_migrations_offline() -> None:
    context.configure(
        url=str(sync_engine.url),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    with sync_engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
