from flask import Blueprint, jsonify, Response
from utils.camera import generate_frames, get_camera_info
from config import Config

camera_bp = Blueprint('camera', __name__)


@camera_bp.route('/api/camera-feed')
def camera_feed():
    return Response(generate_frames(Config.VIDEO_CAPTURE_DEVICE), mimetype='multipart/x-mixed-replace; boundary=frame')

@camera_bp.route('/api/camera-info')
def camera_info():
    camera_info = get_camera_info(Config.VIDEO_CAPTURE_DEVICE)
    return jsonify(camera_info)
