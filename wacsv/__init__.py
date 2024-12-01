from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(disable_autonaming=True)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ChatStorage.sqlite?mode=ro'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WACSV_DATEFORMAT'] = '%a, %d/%m/%Y, %H:%M:%S'
    app.config['WACSV_PAGINATION'] = 200
    app.config['WACSV_TZINFO'] = 'Europe/London'

    # initialize the app with the extension
    db.init_app(app)

    # config jinja2
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    from wacsv.blueprints import main
    app.register_blueprint(main.bp)

    return app
