from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(disable_autonaming=True)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ChatStorage.sqlite?mode=ro'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize the app with the extension
    db.init_app(app)

    from wacsv.blueprints import main
    app.register_blueprint(main.bp)

    return app
