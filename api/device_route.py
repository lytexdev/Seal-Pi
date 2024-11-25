from flask import Blueprint, jsonify, request, current_app
from models import db, Device
from datetime import datetime

device_bp = Blueprint("device", __name__)


@device_bp.route("/api/devices", methods=["GET"])
def list_devices():
    devices = Device.query.all()
    return jsonify(
        [
            {
                "id": device.id,
                "name": device.name,
                "ip": device.ip,
                "last_seen": device.last_seen,
            }
            for device in devices
        ]
    )

@device_bp.route("/api/devices/register", methods=["POST"])
def register_device():
    data = request.json
    name = data.get("name")
    token = data.get("token")
    ip = data.get("ip", request.remote_addr)

    if not name or not token:
        return jsonify({"message": "Device name and token are required"}), 400

    if token != current_app.config["SERVER_TOKEN"]:
        return jsonify({"message": "Invalid token"}), 403

    device = Device.query.filter_by(name=name).first()
    if device:
        device.last_seen = datetime.utcnow()
        device.ip = ip
    else:
        device = Device(name=name, token=token, ip=ip)
        db.session.add(device)

    db.session.commit()
    return jsonify({"message": "Device registered successfully"}), 200
