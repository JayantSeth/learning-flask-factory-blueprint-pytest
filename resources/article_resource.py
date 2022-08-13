from flask_restful import Resource
from flask import request
from models.article import Article
from flask_jwt_extended import jwt_required


class ArticlesResource(Resource):
    @jwt_required()
    def get(self):
        try:
            articles = Article.query.all()
            articles_data = [article.json() for article in articles]
            return {"articles": articles_data}
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500


class ArticleResource(Resource):
    @jwt_required()
    def get(self, title):
        try:
            article = Article.find_by_name(title)
            if not article:
                return {"message": f"Article {title} not found"}, 404
            return {"article": article.json()}
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500

    @jwt_required()
    def post(self, title):
        try:
            article = Article.find_by_name(title)
            if article:
                return {"message": f"Article: {title} already exist"}, 400
            data = request.get_json()
            article = Article(**data)
            article.save_to_db()
            return {"message": f"Article: {title} saved in database"}
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500

    @jwt_required()
    def put(self, title):
        try:
            article = Article.find_by_name(title)
            if not article:
                return {"message": f"Article {title} not found in database"}, 404
            data = request.get_json()
            if 'title' in data:
                article.title = data['title']
            if 'summary' in data:
                article.summary = data['summary']
            if 'author_id' in data:
                article.author_id = data['author_id']
            article.save_to_db()
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500

    @jwt_required(fresh=True)
    def delete(self, title):
        try:
            article = Article.find_by_name(title)
            if not article:
                return {"message": f"Article: {title} does not exist in database"}, 404
            article.delete_from_db()
            return {"message": f"Article: {title} deleted from database"}
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500

