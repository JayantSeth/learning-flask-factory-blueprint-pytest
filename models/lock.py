from utils.database import db


class Lock(db.Model):
    __tablename__ = 'locks'
    id = db.Column(db.Integer, primary_key=True)
    lock_name = db.Column(db.String(25), unique=True, nullable=False)
    key = db.relationship("Key", uselist=False, back_populates="lock")

    def __init__(self, lock_name):
        self.lock_name = lock_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        key = {}
        if self.key:
            key = self.key.json()
        return {"id": self.id, "lock_name": self.lock_name, "key": key}

    @classmethod
    def find_by_name(cls, lock_name):
        return cls.query.filter_by(lock_name=lock_name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def __repr__(self):
        return f"<Lock {self.lock_name}>"

