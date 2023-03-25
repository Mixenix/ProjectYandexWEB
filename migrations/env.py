from __future__ import with_statement

import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context

config = context.config


fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

config.set_main_option(
    'sqlalchemy.url',
    str(current_app.extensions['migrate'].db.get_engine().url).replace(
        '%', '%%'))
target_metadata = current_app.extensions['migrate'].db.metadata


def run_migrations_offline():

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


run_migrations_offline()
