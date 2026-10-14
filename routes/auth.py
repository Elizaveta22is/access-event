from flask import Blueprint, jsonify, request
from models import db, User
from utils.auth_helpers import hash_password, verify_password, generate_token, token_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = data.get("role", "user")
    if not username or not email or not password:
        return jsonify({"message": "Заполните все поля"}), 400
    if role not in ("user", "organizer", "admin"):
        return jsonify({"message": "Недопустимая роль"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email уже зарегистрирован"}), 400
    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        role=role,
        accessibility_needs=data.get("accessibility_needs", ""),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Пользователь создан", "user_id": user.id}), 201


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    user = User.query.filter_by(email=email).first()
    if user is None or not verify_password(password, user.password_hash):
        return jsonify({"message": "Неверный email или пароль"}), 401
    token = generate_token(user.id, user.role)
    return jsonify({"token": token, "role": user.role, "user_id": user.id}), 200


@auth_bp.route("/api/profile", methods=["GET"])
@token_required
def profile(user):
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "accessibility_needs": user.accessibility_needs,
    }), 200
