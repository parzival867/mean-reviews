import sqlite3
import click
from flask import current_app, get_flashed_messages

# more functions

# create the database
def init_db():
	db = get_db()
	with current_app.open_resources('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
	"""clear the existing data and create new tables."""
	init_db()
	click.echo('Initialized the database.')

# more functions