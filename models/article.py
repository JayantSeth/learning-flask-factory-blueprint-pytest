from utils.db import db


class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    summary = db.Column(db.String(300), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))

    @classmethod
    def find_by_name(cls, title):
        return cls.query.filter_by(title=title).first()

    def json(self):
        return {"id": self.id, "title": self.title, "summary": self.summary, "author_id": self.author_id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Article: '{self.title}'>"

