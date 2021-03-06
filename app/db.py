import sqlite3
import click
from flask import current_app, g
#added this
from flask.cli import with_appcontext

# more functions
# connect to database
def connect_db():
	rv = sqlite3.connect(current_app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

# close database connection
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

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
def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)