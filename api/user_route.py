from flask import Blueprint, jsonify, request
from models import db, User

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username, "email": user.email, "is_admin": user.is_admin} for user in users]
    return jsonify(user_list)

@user_bp.route('/api/users', methods=['POST'])
def create_user():
    data = request.json

    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Username, email, and password are required"}), 400

    try:
        new_user = User(
            username=data['username'],
            email=data['email'],
            is_admin=data.get('is_admin', False)
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"message": f"Error creating user: {str(e)}"}), 500

@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    if user:
        try:
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.is_admin = data.get('is_admin', user.is_admin)
            if 'password' in data:
                user.set_password(data['password'])
            db.session.commit()
            return jsonify({"message": "User updated successfully"})
        except Exception as e:
            return jsonify({"message": f"Error updating user: {str(e)}"}), 500
    return jsonify({"message": "User not found"}), 404

@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
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
