from flask import jsonify, request
from app.bp_users import app
from app import db
from app.Models import Users
from app import bcrypt
from app.Helpers import JWT_SecretKey
import jwt
from functools import wraps

@app.route("/register", methods=['POST'])
def Register():
    data = request.get_json()

    existing_email = Users.query.filter_by(email=data['email']).first()

    if(existing_email):
        res = {
            "status": 400,
            "message": "Email already exists! Try logging in"
        }
        return jsonify(res)
    existing_user = Users.query.filter_by(username=data['username']).first()

    if(existing_user):
        res = {
            "status": 400,
            "message": "Username already exists!"
        }
        return jsonify(res)
        

    new_user = Users(data['username'], bcrypt.generate_password_hash(data['password']), data['email'], 'user')
    db.session.add(new_user)
    db.session.commit()

    res = {
        "status": 200,
        "message": "User created successfully! You can login now"
    }
    
    return jsonify(res)

@app.route("/login", methods=["POST"])
def Login():
    data = request.get_json()
    user = Users.query.filter_by(username=data['username']).first()
    if not user:
        res = {
            "status": 400,
            "message": "Invalid username!"
        }
        return jsonify(res)
    
    if(bcrypt.check_password_hash(user.password, data['password'])):
        jwt_token = jwt.encode({
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "email": user.email
        }, key=JWT_SecretKey())
        res = {
            "status": 200,
            "message": "Login successful!",
            "jwt": jwt_token
        }
        return jsonify(res)
    res = {
            "status": 400,
            "message": "Invalid username or password!"
        }
    return jsonify(res)
    
@app.route("/verify", methods=["POST"])
def Verify():
    data = request.get_json()
    jwt_token = request.headers.get("Authorization").split(" ")[1]
    try:
        data = jwt.decode(jwt_token)
        user_id = data['id']
        user = Users.query.filter_by(id = user_id).first()
        if user:
            return jsonify({
                "status": 200,
                "message": "Verified session!"
            })
        else:
            return jsonify({
            "status": 400,
            "message": "Invalid JWT Token!"
        })
    except:
        return jsonify({
            "status": 400,
            "message": "Invalid JWT Token!"
        })
