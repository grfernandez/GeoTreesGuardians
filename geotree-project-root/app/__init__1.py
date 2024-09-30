from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

def create_app(test_config=None):
    # Crear la aplicación Flask
    app = Flask(__name__, instance_relative_config=True)

    # Cargar la configuración desde un objeto de configuración
    app.config.from_object('app.config.Config')

    # Inicializar las bd
    geotree = SQLAlchemy(app)
    redis_client = FlaskRedis(app)

    # Importar las rutas de la aplicación
    from app import routes

    return app

