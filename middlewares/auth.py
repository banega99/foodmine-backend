from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps


def auth_middleware(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            request.user = current_user
        except:
            return jsonify({"msg": "Unauthorized"}), 401
        return fn(*args, **kwargs)

    return wrapper
