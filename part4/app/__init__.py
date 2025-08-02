from flask import Flask, render_template  # ← render_template を忘れずに
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as place_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.admin import api as admin_users

    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Add a JWT with **Bearer <JWT>**"
        }
    }

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        authorizations=authorizations,
        security='Bearer Auth'
    )

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(place_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(admin_users, path="/api/v1/admin/users")

    # ✅ HTMLページ用ルーティング
    @app.route('/login.html')
    def login_page():
        return render_template('login.html')

    @app.route('/index.html')
    def index_page():
        return render_template('index.html')

    with app.app_context():
        db.create_all()
        seed_users()

    return app

def seed_users():
    from app.services import facade
    email = "admin@example.com"
    user = facade.get_user_by_email(email)
