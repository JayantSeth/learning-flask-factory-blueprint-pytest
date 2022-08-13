from flask_restful import Resource
from flask import request
from models.author import Author


class AuthorsResource(Resource):
    def get(self):
        try:
            authors_data = Author.query.all()
            authors = [author.json() for author in authors_data]
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
        return {'authors': authors}


class AuthorResource(Resource):
    def get(self, name):
        author = Author.find_by_name(name)
        if author:
            return author.json()
        return {"message": f"Author: {name} not found"}, 400

    def post(self, name):
        author = Author.find_by_name(name)
        if author:
            return {"message": f"Author {name} already exist"}, 400
        data = request.get_json()
        author = Author(**data)
        try:
            author.save_to_db()
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
        return {"message": f"Author {name} saved to database"}

    def put(self, name):
        author = Author.find_by_name(name)
        if not author:
            return {"message": f"Author {name} does not exist"}, 400
        data = request.get_json()
        author.name = data['name']
        author.email = data['email']
        try:
            author.save_to_db()
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
        return {"message": f"Author {name} updated to database"}

    def delete(self, name):
        author = Author.find_by_name(name)
        if not author:
            return {"message": f"Author {name} does not exist"}, 400
        try:
            author.delete_from_db()
        except BaseException as e:
            return {"message": f"Error {e}"}, 500
        return {"message": f"Author {name} deleted from database"}