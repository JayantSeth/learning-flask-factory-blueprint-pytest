from utils.database import db

student_subject = db.Table('student_subject',
                           db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
                           db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True)
                           )


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    class_name = db.Column(db.String, nullable=False)
    subjects = db.relationship('Subject', secondary=student_subject, lazy='subquery',
                               backref=db.backref('students', lazy=True))

    def __init__(self, name, class_name):
        self.name = name
        self.class_name = class_name

    def json(self):
        subjects = [subject.json() for subject in self.subjects]
        return {'id': self.id, 'name': self.name, 'class_name': self.class_name, 'subjects': subjects}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Student '{self.name}'>"
