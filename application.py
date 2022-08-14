from flask import Blueprint, Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
import os


def create_app(ENVIRONMENT="DEVELOPMENT"):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    if ENVIRONMENT == "DEVELOPMENT":
        app.config.from_object('config.DevConfig')
    elif ENVIRONMENT == "TESTING":
        # if test db is present delete the same
        if os.path.exists("test_data.db"):
            os.remove("test_data.db")
        app.config.from_object('config.TestConfig')
    else:
        app.config.from_object('config.ProdConfig')
    with app.app_context():
        auth_bp = Blueprint("auth_bp", __name__)
        app_bp = Blueprint("app_bp", __name__)
        jwt = JWTManager(app)
        auth_api = Api(auth_bp)
        app_api = Api(app_bp)
        from resources.auth_resource import SignUp, SignIn, RefreshToken
        from resources.author_resource import AuthorsResource, AuthorResource
        from resources.article_resource import ArticlesResource, ArticleResource
        auth_api.add_resource(SignUp, '/signup')
        auth_api.add_resource(SignIn, '/signin')
        auth_api.add_resource(RefreshToken, '/refresh_token')
        app_api.add_resource(ArticlesResource, '/articles')
        app_api.add_resource(ArticleResource, '/article/<string:title>')
        app_api.add_resource(AuthorsResource, '/authors')
        app_api.add_resource(AuthorResource, '/author/<string:name>')
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(app_bp, url_prefix="/api")
        from utils.db import db
        db.init_app(app)
        db.create_all()
    return app




