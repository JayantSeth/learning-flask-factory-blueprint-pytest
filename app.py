from flask import Blueprint, Flask
from utils.db import db
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from resources.auth_resource import SignUp, SignIn, RefreshToken
from resources.author_resource import AuthorsResource, AuthorResource
from resources.article_resource import ArticlesResource, ArticleResource

auth_bp = Blueprint("auth_bp", __name__)

app_bp = Blueprint("app_bp", __name__)

app = Flask(__name__)

ENVIRONMENT = "DEVELOPMENT"

app.config.from_object('config.Config')

if ENVIRONMENT == "DEVELOPMENT":
    app.config.from_object('config.DevConfig')
else:
    app.config.from_object('config.ProdConfig')

jwt = JWTManager(app)

auth_api = Api(auth_bp)

app_api = Api(app_bp)

auth_api.add_resource(SignUp, '/signup')
auth_api.add_resource(SignIn, '/signin')
auth_api.add_resource(RefreshToken, '/refresh_token')

app_api.add_resource(ArticlesResource, '/articles')
app_api.add_resource(ArticleResource, '/article/<string:title>')
app_api.add_resource(AuthorsResource, '/authors')
app_api.add_resource(AuthorResource, '/author/<string:name>')

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(app_bp, url_prefix="/api")


if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)




