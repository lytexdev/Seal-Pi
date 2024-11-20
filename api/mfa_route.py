from flask import Blueprint, jsonify, request, session
import pyotp
import secrets
from models import db, User

mfa_bp = Blueprint("mfa", __name__)

@mfa_bp.route("/api/mfa/setup-totp", methods=["POST"])
def setup_totp():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"message": "User not logged in"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    secret = pyotp.random_base32()
    user.mfa_type = "TOTP"
    user.mfa_secret = secret
    db.session.commit()

    totp = pyotp.TOTP(secret)
    otp_url = totp.provisioning_uri(name=user.email, issuer_name="Seal-Pi")

    return (jsonify({"message": "TOTP setup initiated", "secret": secret, "otp_url": otp_url}), 200)

@mfa_bp.route("/api/mfa/verify-totp", methods=["POST"])
def verify_totp():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"message": "User not logged in"}), 401

    data = request.json
    totp_code = data.get("totp_code")

    user = User.query.get(user_id)
    if not user or user.mfa_type != "TOTP" or not user.mfa_secret:
        return jsonify({"message": "TOTP is not set up for this user"}), 400

    totp = pyotp.TOTP(user.mfa_secret)
    if not totp.verify(totp_code, valid_window=1):  # Allow 1 code before and after
        return jsonify({"message": "Invalid TOTP code"}), 400

    backup_codes = user.generate_backup_codes()
    user.mfa_enabled = True
    db.session.commit()

    return (jsonify({"message": "TOTP verified successfully", "backup_codes": backup_codes}), 200)

@mfa_bp.route("/api/mfa/status", methods=["GET"])
def mfa_status():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"message": "User not logged in"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return (jsonify({"totp_enabled": user.mfa_type == "TOTP" and user.mfa_enabled}), 200)

@mfa_bp.route("/api/mfa/delete-totp", methods=["POST"])
def delete_totp():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"message": "User not logged in"}), 401

    user = User.query.get(user_id)
    if not user or user.mfa_type != "TOTP":
        return jsonify({"message": "TOTP is not set up"}), 400

    user.mfa_enabled = False
    user.mfa_type = None
    user.mfa_secret = None
    user.backup_codes = None
    db.session.commit()

    return jsonify({"message": "TOTP deleted successfully"}), 200
