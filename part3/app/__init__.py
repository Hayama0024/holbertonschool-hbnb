from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import DevelopmentConfig

db = SQLAlchemy()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from app.routes.users import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/v1/users')

    with app.app_context():
        # ⚠️ Userのインポートはappとdbの初期化の後！
        from app.models.user import User
        db.create_all()

    return app
