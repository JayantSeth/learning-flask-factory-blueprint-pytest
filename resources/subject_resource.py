from flask_restful import Resource
from models.subject import Subject


from flask import request


class SubjectsResource(Resource):
    def get(self):
        try:
            subjects_data = Subject.query.all()
            subjects = [subject.json() for subject in subjects_data]
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
        return {"subjects": subjects}


class SubjectResource(Resource):
    def get(self, subject):
        subject = Subject.find_by_subject(subject)
        if subject:
            return subject.json()
        return {"message": "Subject not found"}

    def post(self, subject):
        if Subject.find_by_subject(subject):
            return {"message": "Subject already exist"}, 400
        data = request.get_json()
        subject = Subject(**data)
        try:
            subject.save_to_db()
        except BaseException as e:
            return {"message": f"Error {e}"}, 500
        return subject.json()

    def put(self, subject):
        subject = Subject.find_by_subject(subject)
        if subject:
            data = request.get_json()
            subject.subject = data['subject']
            try:
                subject.save_to_db()
            except BaseException as e:
                return {"message": f"Error: {e}"}, 500
            return subject.json()
        return {"message": f"Subject {subject} does not exist"}, 400

    def delete(self, subject):
        subject = Subject.find_by_subject(subject)
        try:
            subject.delete_from_db()
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
        return {"message": f"Subject: {subject} is deleted successfully"}
