from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import DevelopmentConfig

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)

    from app.routes.users import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/v1/users')

    with app.app_context():
        from app.models.user import User
        db.create_all()

    return app
