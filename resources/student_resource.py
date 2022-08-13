from models.student import Student
from flask_restful import Resource
from flask import request
from models.subject import Subject


class StudentsResource(Resource):
    def get(self):
        try:
            student_data = Student.query.all()
            students = [student.json() for student in student_data]
            return {"students": students}
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500


class StudentResource(Resource):
    def get(self, name):
        try:
            student = Student.find_by_name(name)
            if student:
                return {"student": student.json()}
            return {"message": f"Student: {name} not found in database"}
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500

    def post(self, name):
        try:
            student = Student.find_by_name(name)
            if student:
                return {"message": f"Student: {student} already exist"}, 400
            student_data = request.get_json()
            student = Student(student_data['name'], student_data['class_name'])
            try:
                for subject in student_data['subjects']:
                    sub = Subject.find_by_subject(subject)
                    student.subjects.append(sub)
                student.save_to_db()
                return {"message": f"Student: {name} successfully saved in database"}
            except BaseException as e:
                return {"message": f"Error: {e}"}
        except BaseException as e:
            return {"message": f"Error: {e}"}

    def put(self, name):
        try:
            student = Student.find_by_name(name)
            if not student:
                return {"message": f"Student: {name} not found in database"}, 400
            student_data = request.get_json()
            if 'name' in student_data:
                student.name = student_data['name']
            if 'class_name' in student_data:
                student.class_name = student_data['class_name']
            if 'subjects' in student_data:
                for subject in student_data['subjects']:
                    sub = Subject.find_by_subject(subject)
                    student.subjects.append(sub)
            try:
                student.save_to_db()
                return {"message": f"Student: {name} updated successfully"}
            except BaseException as e:
                return {"message": f"Error: {e}"}, 500
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500

    def delete(self, name):
        try:
            student = Student.find_by_name(name)
            if not student:
                return {"message": f"Student: {name} not found in database"}
            try:
                student.delete_from_db()
                return {"message": f"Student: {name} deleted successfully"}
            except BaseException as e:
                return {"message": f"Error: {e}"}
        except BaseException as e:
            return {"message": f"Error: {e}"}
