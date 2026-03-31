import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from app.models.product import Base
import os
from dotenv import load_dotenv


load_dotenv()
config = context.config

database_url = os.getenv("DATABASE_URL")


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata





def run_migrations_offline() -> None:

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

# COMO DEVE FICAR (COPIE ESTE BLOCO)
async def run_async_migrations() -> None:
    
    section = config.get_section(config.config_ini_section, {})
    
    db_url = os.getenv("DATABASE_URL")
    
    if db_url:
        section["sqlalchemy.url"] = db_url

    connectable = async_engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
