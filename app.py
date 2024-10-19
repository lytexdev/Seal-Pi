from flask import Flask, render_template, Response, jsonify
from config import Config
from util.camera import generate_frames, get_camera_info

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/camera-feed')
def camera_feed():
    return Response(generate_frames(Config.VIDEO_CAPTURE_DEVICE), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/camera-info')
def camera_info():
    camera_info = get_camera_info(Config.VIDEO_CAPTURE_DEVICE)
    return jsonify(camera_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
