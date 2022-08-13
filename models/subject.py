from utils.database import db


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(25), nullable=False, unique=True)

    def __init__(self, subject):
        self.subject = subject

    def json(self):
        return {'id': self.id, 'subject': self.subject}

    @classmethod
    def find_by_subject(cls, subject):
        return cls.query.filter_by(subject=subject).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Subject '{self.subject}'>"

