import jwt
import datetime
from config import TOKEN_EXP, TOKEN_SECRET, TOKEN_ALGO


def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=TOKEN_EXP),
    }

    return jwt.encode(payload=payload, key=TOKEN_SECRET, algorithm=TOKEN_ALGO)


def verify_token(token):
    try:
        payload = jwt.decode(jwt=token, key=TOKEN_SECRET, algorithms=TOKEN_ALGO)
        return {"status": "Valid Token"}, True

    except jwt.exceptions.ExpiredSignatureError:
        return {"status": "Token Expired"}, False

    except jwt.exceptions.InvalidTokenError:
        return {"status": "Invalid Token"}, False
