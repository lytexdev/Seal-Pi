from flask import Flask, render_template, request, Response, jsonify, send_from_directory

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

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(user_list)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Username, email, and password are required"}), 400

    try:
        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        app.logger.error(f"Error creating user: {str(e)}")
        return jsonify({"message": "Error creating user"}), 500

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    if user:
        try:
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            if 'password' in data:
                user.set_password(data['password'])
            db.session.commit()
            return jsonify({"message": "User updated successfully"})
        except Exception as e:
            app.logger.error(f"Error updating user: {str(e)}")
            
    return jsonify({"message": "User not found"}), 404

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"})
        except Exception as e:
            return jsonify({"message": "Error deleting user"}), 500
    return jsonify({"message": "User not found"}), 404

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
