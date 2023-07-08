from flask import jsonify, request
from app.Models import Users
import jwt
from functools import wraps

def VerifyJWT(f):
    @wraps(f)
    def verify():
        data = request.get_json()
        jwt_token = request.headers.get("Authorization").split(" ")[1]
        try:
            data = jwt.decode(jwt_token)
            user_id = data.id
            user = Users.query.filter_by(id = user_id).first()
            if user:
                request.user = user
                return f()
            else:
                return jsonify({
                "status": 400,
                "message": "Invalid JWT Token!"
            })
        except Exception as e:
            return jsonify({
                "status": 400,
                "message": "Invalid JWT Token!", 
                "error": e
            })
    return verify