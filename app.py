from flask import Flask, render_template, Response, jsonify, send_from_directory

from config import Config
from models import db, User
from utils.camera import generate_frames, get_camera_info

app = Flask('Seal-Pi', template_folder='templates', static_folder='static')
app.secret_key = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.after_request
def add_header(response):
    response.headers['X-Robots-Tag'] = 'noindex, nofollow'
    return response

@app.route('/robots.txt')
def robots_txt():
    try:
        return Response("User-agent: *\nDisallow: /", mimetype="text/plain")
    except Exception as e:
        app.logger.error(f"Error generating robots.txt: {str(e)}")
        return Response("Error generating robots.txt", status=500)

@app.route('/api/camera-feed')
def camera_feed():
    return Response(generate_frames(Config.VIDEO_CAPTURE_DEVICE), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/camera-info')
def camera_info():
    camera_info = get_camera_info(Config.VIDEO_CAPTURE_DEVICE)
    return jsonify(camera_info)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

def init_db():
    with app.app_context():
        db.create_all()
        app.logger.info("Database initialized")

init_db()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=Config.PORT, debug=True)
    except Exception as e:
        app.logger.error(f"Error starting server: {str(e)}")
