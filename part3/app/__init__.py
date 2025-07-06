from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from app import config


bcrypt = Bcrypt()

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)

    api = Api(app)

    from app.api.v1.users import api as user_bp
    api.add_namespace(user_bp, path='/api/v1/users')

    return app
