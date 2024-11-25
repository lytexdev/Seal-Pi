import time
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    mfa_enabled = db.Column(db.Boolean, default=False, nullable=False)
    mfa_type = db.Column(db.String(20))
    mfa_secret = db.Column(db.String(120))
    backup_codes = db.Column(db.Text)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_backup_codes(self, count=8):
        import secrets

        codes = [secrets.token_hex(8) for _ in range(count)]
        self.backup_codes = ",".join(codes)
        return codes


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    token = db.Column(db.String(120), nullable=False, unique=True)
    ip = db.Column(db.String(120), nullable=False)
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))


if __name__ == '__main__':
    db.create_all()
