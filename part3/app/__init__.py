from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from app import config
from flask_jwt_extended import JWTManager


bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    jwt.init_app(app)

    api = Api(app)

    from app.api.v1.users import api as user_bp
    api.add_namespace(user_bp, path='/api/v1/users')
    from app.api.v1.auth import api as auth_ns
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
