from flask_restful import Resource
from flask import request
from models.key import Key


class KeysResource(Resource):
    def get(self):
        try:
            keys = Key.query.all()
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
        keys_data = [key.json() for key in keys]
        return {"keys": keys_data}


class KeyResource(Resource):
    def get(self, key_name):
        try:
            key = Key.find_by_name(key_name)
            if not key:
                return {"message": f"Key: {key_name} not found in database"}, 404
        except BaseException as e:
            return {"message": f"Error: {e}"}
        key_json = key.json()
        return {"key": key_json}

    def post(self, key_name):
        try:
            key = Key.find_by_name(key_name)
            if key:
                return {"message": f"Key: {key_name} already exist"}, 400
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
        key_data = request.get_json()
        key = Key(**key_data)
        try:
            key.save_to_db()
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
        return {"message": f"Key: {key} saved in database"}

    def put(self, key_name):
        try:
            key = Key.find_by_name(key_name)
            if not key:
                return {"message": f"Key: {key} does not exist in database"}, 404
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
        key_data = request.get_json()
        if 'key_name' in key_data:
            key.key_name = key_data['key_name']
        if 'lock_id' in key_data:
            key.lock_id = key_data['lock_id']
        try:
            key.save_to_db()
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
        return {"message": f"Key: {key} updated successfully"}

    def delete(self, key_name):
        try:
            key = Key.find_by_name(key_name)
            if not key:
                return {"message": f"Key: {key_name} does not exist in database"}, 404
            key.delete_from_db()
            return {"message": f"Key: {key} deleted from database"}
        except BaseException as e:
            return {"message": f"Error: {e}"}, 500
