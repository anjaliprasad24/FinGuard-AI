from logging.config import fileConfig
from pathlib import Path
import sys

from alembic import context
from sqlalchemy import engine_from_config, event, pool

# Ensure backend root directory is in sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from app.models import Base  # Explicitly imports all 6 domain models into metadata

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Set SQLAlchemy database URL dynamically from application settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Target metadata for autogenerate support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Configures the context with just a URL and not an Engine.
    """
    url = config.get_main_option("sqlalchemy.url")
    is_sqlite = url.startswith("sqlite") if url else False

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=is_sqlite,
    )

    with context.begin_transaction():
        context.run_migrations()


def configure_context_and_run(connection) -> None:
    """Configure Alembic migration context with an active database connection and execute migrations."""
    url = config.get_main_option("sqlalchemy.url")
    is_sqlite = (url and url.startswith("sqlite")) or connection.dialect.name == "sqlite"

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=is_sqlite,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Creates an Engine and associates a connection with the context.
    """
    connectable = config.attributes.get("connection", None)

    if connectable is None:
        url = config.get_main_option("sqlalchemy.url")
        connect_args = {}
        if url and url.startswith("sqlite"):
            connect_args["check_same_thread"] = False

        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            connect_args=connect_args,
        )

        if url and url.startswith("sqlite"):
            @event.listens_for(connectable, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record) -> None:
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

        with connectable.connect() as connection:
            configure_context_and_run(connection)

        connectable.dispose()
    else:
        configure_context_and_run(connectable)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
