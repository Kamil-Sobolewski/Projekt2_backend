from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
mm = Marshmallow()
jwt = JWTManager()
cors = CORS(supports_credentials=True, origins='http://127.0.0.1:8080')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    mm.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    from .routes.account_routes import bp as acc_bp
    app.register_blueprint(acc_bp)
    from .routes.auth_routes import bp as auth_bp
    app.register_blueprint(auth_bp)
    from .routes.product_routes import bp as prod_bp
    app.register_blueprint(prod_bp)

    return app


from .models.product_models import Product, Category
from .models.account_models import Account, Role, Permission
