    # Logging modules for tracking migration events and errors
import logging
from logging.config import fileConfig

# Access Flask app context (needed to get database connection)
from flask import current_app

# Alembic core module for database migrations
from alembic import context


# Alembic configuration object (reads alembic.ini file)
config = context.config

# Configure logging using alembic.ini settings
fileConfig(config.config_file_name)

# Create logger for Alembic environment
logger = logging.getLogger('alembic.env')

# Function to get database engine (connection handler)
def get_engine():
    try:
        # For Flask-SQLAlchemy older versions
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # For Flask-SQLAlchemy 3+
        return current_app.extensions['migrate'].db.engine


# Function to get database URL (connection string)
def get_engine_url():
    try:
        # Returns database URL safely (hides password issues)
        return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')


# Set database URL in Alembic config dynamically
config.set_main_option('sqlalchemy.url', get_engine_url())

# Get database object from Flask-Migrate extension
target_db = current_app.extensions['migrate'].db


# Returns metadata (table structure definitions from models)
def get_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


# Runs migrations without a live database connection
def run_migrations_offline():

    url = config.get_main_option("sqlalchemy.url")

    # Configure Alembic in offline mode
    context.configure(
        url=url,
        target_metadata=get_metadata(),
        literal_binds=True
    )

    # Start migration transaction
    with context.begin_transaction():
        context.run_migrations()


# Runs migrations with an active database connection
def run_migrations_online():

    # Prevents empty migrations from being generated
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]

            # If no schema changes detected, skip migration
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    # Get migration configuration arguments
    conf_args = current_app.extensions['migrate'].configure_args

    # Attach custom revision handler if not already set
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    # Get database engine
    connectable = get_engine()

    # Establish database connection
    with connectable.connect() as connection:

        # Configure Alembic with connection and metadata
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        # Run migration inside transaction
        with context.begin_transaction():
            context.run_migrations()


# Decide whether to run offline or online migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
