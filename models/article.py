from utils.database import db


class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    summary = db.Column(db.String(300), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))

    def __init__(self, author_id, title, summary):
        self.author_id = author_id
        self.title = title
        self.summary = summary

    def json(self):
        return {'id': self.id, 'title': self.title, 'summary': self.summary, 'author_id': self.author_id}

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __str__(self):
        return f"Title: {self.title} Author ID: {self.author_id}"
