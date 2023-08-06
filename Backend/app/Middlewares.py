from flask import jsonify, request
from app.Models import Users
from app.Helpers import JWT_SecretKey
import jwt
from functools import wraps

def VerifyJWT(f):
    @wraps(f)
    def verify():
        try:
            jwt_token = request.headers.get("Authorization").split(" ")[1]
            try:
                data = jwt.decode(jwt_token, key=JWT_SecretKey(), algorithms=['HS256'])
                user_id = data['id']
                user = Users.query.filter_by(id = user_id).first()
                if user:
                    request.user = user
                    return f()
                else:
                    return jsonify(message = "Invalid User Data!"), 400
            except Exception as e:
                print(e)
                return jsonify(message = "Invalid JWT Token!"), 400
        except Exception as e:
            print(e)
            return jsonify(message="JWT Token not provided"), 400
    return verify

def isAdmin(f):
    @wraps(f)
    def isAdmin():
        if request.user.role == "admin": return f()
        return jsonify(message="Access denied"), 401
    return isAdmin