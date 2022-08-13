from flask_restful import Resource
from flask import request
from models.lock import Lock
from models.key import Key


class LocksResource(Resource):
    def get(self):
        try:
            locks = Lock.query.all()
            locks_data = [lock.json() for lock in locks]
            return {"locks": locks_data}
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500


class LockResource(Resource):
    def get(self, lock_name):
        try:
            lock = Lock.find_by_name(lock_name)
            if lock:
                return {"lock": lock.json()}
            return {"message": f"Lock: {lock_name} not found in database"}, 404
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500

    def post(self, lock_name):
        try:
            lock = Lock.find_by_name(lock_name)
            if lock:
                return {"message": f"Lock: {lock_name} already exist"}, 400
            lock_data = request.get_json()
            lock = Lock(**lock_data)
            try:
                lock.save_to_db()
                return {"message": f"Lock: {lock} saved in database"}
            except BaseException as e:
                return {"message": f"Error: {e}"}, 500
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500

    def put(self, lock_name):
        try:
            lock = Lock.find_by_name(lock_name)
            if not lock:
                return {"message": f"Lock {lock_name} does not exist in database"}, 404
            lock_data = request.get_json()
            if 'lock_name' in lock_data:
                lock.lock_name = lock_data['lock_name']
            if 'key' in lock_data:
                try:
                    key = Key.find_by_name(lock_data['key'])
                    if key:
                        lock.key = key
                except BaseException as e:
                    return {"message": f"Error: {e}"}, 500
            lock.save_to_db()
            return {"message": f"Lock: {lock} updated successfully"}
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500

    def delete(self, lock_name):
        try:
            lock = Lock.find_by_name(lock_name)
            if not lock:
                return {"message": f"Lock: {lock_name} does not exist in database"}, 404
            lock.delete_from_db()
            return {"message": f"Lock: {lock} deleted from database"}
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
