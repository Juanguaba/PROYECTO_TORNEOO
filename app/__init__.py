from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Configuración
    app.config.from_object("config.Config")

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar modelos
    from app import models

    # Registrar Blueprints
    from app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.admin import admin_bp
    app.register_blueprint(admin_bp)

    from app.equipos import equipos_bp
    app.register_blueprint(equipos_bp)

    return app
