from models.article import Article
from flask_restful import Resource
from flask import request


class ArticlesResource(Resource):
    def get(self):
        try:
            articles_data = Article.query.all()
            articles = [article.json() for article in articles_data]
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
        return {"articles": articles}


class ArticleResource(Resource):
    def get(self, title):
        article = Article.find_by_title(title)
        if article:
            return article.json()
        return {"message": "Article not found"}

    def post(self, title):
        if Article.find_by_title(title):
            return {"message": "Article with this title already exist"}, 400
        data = request.get_json()
        article = Article(**data)
        try:
            article.save_to_db()
        except BaseException as e:
            return {"message": f"Error {e}"}, 500
        return article.json()

    def put(self, title):
        article = Article.find_by_title(title)
        if article:
            data = request.get_json()
            article.title = data['title']
            article.summary = data['summary']
            article.author_id = data['author_id']
            try:
                article.save_to_db()
            except BaseException as e:
                return {"message": f"Error: {e}"}, 500
            return article.json()
        return {"message": f"Article with Title: {title} does not exist"}, 400

    def delete(self, title):
        article = Article.find_by_title(title)
        try:
            article.delete_from_db()
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
        return {"message": f"Article: {title} is deleted successfully"}


