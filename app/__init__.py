# __init__.py

import os
from flask import Flask

def create_app(config_file=None):
	# create and configure the app
	app = Flask(__name__)

	# configuration
	if (config_name is not None):
		app.config.from_pyfile(config_file, silent=True)
	else:
		app.config.from_mapping(
			SECRET_KEY='dev',
			DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
		)

	# attach routes/ views and database functions
	from . import db
	db.init_app(app)

	return app