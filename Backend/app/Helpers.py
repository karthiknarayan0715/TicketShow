import jwt
def JWT_SecretKey():
    return "secret_key"

def DecodeJWT(jwt_token):
    try:
        data = jwt.decode(jwt_token, key=JWT_SecretKey(), algorithms=['HS256'])
    except Exception as e:
        raise Exception("Invalid JWT Token")