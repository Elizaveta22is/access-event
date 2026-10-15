import datetime
import functools
import jwt
from flask import current_app, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User


def hash_password(password):
    return generate_password_hash(password)


def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)


def generate_token(user):
    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def token_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"message": "Токен отсутствует"}), 401
        token = auth_header.split("Bearer ", 1)[1]
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Срок действия токена истёк"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Неверный токен"}), 401
        user = db.session.get(User, data.get("user_id"))
        if user is None:
            return jsonify({"message": "Пользователь не найден"}), 401
        return f(user=user, *args, **kwargs)
    return wrapper


def role_required(*roles):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(user, *args, **kwargs):
            if user.role not in roles:
                return jsonify({"message": "Недостаточно прав"}), 403
            return f(user=user, *args, **kwargs)
        return wrapper
    return decorator
