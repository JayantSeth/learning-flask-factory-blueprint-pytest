from utils.database import db


class Key(db.Model):
    __tablename__ = 'keys'
    id = db.Column(db.Integer, primary_key=True)
    key_name = db.Column(db.String(25), unique=True, nullable=False)
    lock_id = db.Column(db.Integer, db.ForeignKey('locks.id'), unique=True)
    lock = db.relationship("Lock", back_populates="key")

    def __init__(self, key_name, lock_id):
        self.key_name = key_name
        self.lock_id = lock_id

    def json(self):
        return {"id": self.id, "key_name": self.key_name, "lock_id": self.lock_id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Key '{self.key_name}>"

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(key_name=name).first()
