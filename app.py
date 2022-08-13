from flask import Flask
from flask_restful import Api

from resources.article_resource import ArticlesResource, ArticleResource
from resources.author_resource import AuthorsResource, AuthorResource
from resources.subject_resource import SubjectsResource, SubjectResource
from resources.student_resource import StudentsResource, StudentResource
from resources.lock_resource import LocksResource, LockResource
from resources.key_resource import KeysResource, KeyResource

from utils.database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)


api.add_resource(ArticleResource, '/article/<string:title>')
api.add_resource(ArticlesResource, '/articles')
api.add_resource(AuthorResource, '/author/<string:name>')
api.add_resource(AuthorsResource, '/authors')
api.add_resource(SubjectsResource, '/subjects')
api.add_resource(SubjectResource, '/subject/<string:subject>')
api.add_resource(StudentsResource, '/students')
api.add_resource(StudentResource, '/student/<string:name>')
api.add_resource(LocksResource, '/locks')
api.add_resource(LockResource, '/lock/<string:lock_name>')
api.add_resource(KeysResource, '/keys')
api.add_resource(KeyResource, '/key/<string:key_name>')


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
