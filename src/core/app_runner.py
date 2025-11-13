from flask import Flask
from flask_migrate import Migrate

from src.core.config import settings
from src.core.db import db

from src import models
from src.routers.categories import categories_bp


def init_database(app: Flask) -> None:
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)


def register_routers(app: Flask) -> None:
    from src.routers.questions import questions_bp

    app.register_blueprint(questions_bp)
    app.register_blueprint(categories_bp)



def create_app(app: Flask) -> None:
    app.config.update(settings.get_flask_config())

    init_database(app)
    register_routers(app)
