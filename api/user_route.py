from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash
import pyotp
from models import db, User

user_bp = Blueprint("user", __name__)


@user_bp.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
        }
        for user in users
    ]
    return jsonify(user_list)


@user_bp.route("/api/users", methods=["POST"])
def create_user():
    data = request.json

    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Username, email, and password are required"}), 400

    try:
        new_user = User(
            username=data["username"],
            email=data["email"],
            is_admin=data.get("is_admin", False),
        )
        new_user.set_password(data["password"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"message": f"Error creating user: {str(e)}"}), 500


@user_bp.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    if user:
        try:
            user.username = data.get("username", user.username)
            user.email = data.get("email", user.email)
            user.is_admin = data.get("is_admin", user.is_admin)
            if "password" in data:
                user.set_password(data["password"])
            db.session.commit()
            return jsonify({"message": "User updated successfully"})
        except Exception as e:
            return jsonify({"message": f"Error updating user: {str(e)}"}), 500

    return jsonify({"message": "User not found"}), 404


@user_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"})
        except Exception as e:
            return jsonify({"message": f"Error deleting user: {str(e)}"}), 500

    return jsonify({"message": "User not found"}), 404


@user_bp.route("/api/user-status", methods=["GET"])
def get_user_status():
    user_id = session.get("user_id")
    is_admin = session.get("is_admin", False)
    if user_id:
        return jsonify({"is_logged_in": True, "is_admin": is_admin}), 200

    return jsonify({"is_logged_in": False, "is_admin": False}), 200


@user_bp.route("/api/login", methods=["POST"])
def login_user():
    data = request.json
    identifier = data.get("username_or_email")
    password = data.get("password")
    totp_code = data.get("totp_code")

    if not identifier or not password:
        return jsonify({"message": "Username/Email and password are required"}), 400

    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username/email or password"}), 401

    if user.mfa_enabled and user.mfa_type == "TOTP":
        if not totp_code:
            return jsonify({"message": "TOTP code is required"}), 400
        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(totp_code, valid_window=1):
            return jsonify({"message": "Invalid TOTP code"}), 400

    session["user_id"] = user.id
    session["is_admin"] = user.is_admin
    session["mfa_verified"] = user.mfa_enabled
    return jsonify({"message": "Login successful", "is_admin": user.is_admin}), 200

@user_bp.route("/api/logout", methods=["POST"])
def logout_user():
    session.pop("user_id", None)
    session.pop("is_admin", None)
    session.pop("mfa_verified", None)  # Remove MFA session status
    return jsonify({"message": "Logout successful"}), 200
