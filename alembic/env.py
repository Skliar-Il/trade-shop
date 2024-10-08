from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context




import os, sys 

sys.path.append(os.path.join(sys.path[0][:-7], "src"))



from models.admins import *
from models.products import * 
from models.photo import *
from models.blog import *
from database import Base

from config import POSTGRES_HOST, POSTGRES_NAME, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER



config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
    
session = config.config_ini_section
config.set_section_option(session, "POSTGRES_PASSWORD", POSTGRES_PASSWORD)
config.set_section_option(session, "POSTGRES_NAME", POSTGRES_NAME)
config.set_section_option(session, "POSTGRES_USER", POSTGRES_USER)
config.set_section_option(session, "POSTGRES_HOST", POSTGRES_HOST)
config.set_section_option(session, "POSTGRES_PORT", POSTGRES_PORT)


target_metadata = Base.metadata




def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
