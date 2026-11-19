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

    from app.jugadores import jugadores_bp
    app.register_blueprint(jugadores_bp)

    from app.torneos import torneos_bp
    app.register_blueprint(torneos_bp)

    from app.partidos import partidos_bp
    app.register_blueprint(partidos_bp)

    from app.estadios import estadios_bp
    app.register_blueprint(estadios_bp)

    from app.arbitros import arbitros_bp
    app.register_blueprint(arbitros_bp)

    from app.configuracion import configuracion_bp
    app.register_blueprint(configuracion_bp)

    from app.utils.date import calcular_edad
    app.jinja_env.globals["calcular_edad"] = calcular_edad

    return app
