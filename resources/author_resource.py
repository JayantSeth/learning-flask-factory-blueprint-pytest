from models.author import Author
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended.exceptions import FreshTokenRequired


class AuthorsResource(Resource):
    @jwt_required()
    def get(self):
        try:
            authors = Author.query.all()
            authors_data = [author.json() for author in authors]
            return {"authors": authors_data}
        except BaseException as e:
            return {"message": f"Error: {e}"}


class AuthorResource(Resource):
    @jwt_required()
    def get(self, name):
        try:
            author = Author.find_by_name(name)
            if not author:
                return {"message": f"Author: {name} not found in database"}, 404
            return {"author": author.json()}
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500

    @jwt_required()
    def post(self, name):
        try:
            author = Author.find_by_name(name)
            if author:
                return {"message": f"Author: {name} already exist"}, 400
            author_data = request.get_json()
            author = Author(**author_data)
            author.save_to_db()
            return {"message": f"Author {author} saved in database"}
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500

    @jwt_required()
    def put(self, name):
        try:
            author = Author.find_by_name(name)
            if not author:
                return {"message": f"Author: {name} does not exist in database"}, 404
            data = request.get_json()
            if 'name' in data:
                author.name = data['name']
            if 'age' in data:
                author.age = data['age']
            author.save_to_db()
            return {"message": f"Author: {name} updated successfully"}
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500

    @jwt_required(fresh=True)
    def delete(self, name):
        try:
            author = Author.find_by_name(name)
            if not author:
                return {"message": f"Author: {name} does not exist in database"}, 404
            author.delete_from_db()
            return {"message": f"Author: {name} deleted from database"}
        except FreshTokenRequired:
            return {"message": "Fresh token required"}, 400
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
