from flask import Flask, render_template, Response
from dotenv import load_dotenv
import os
import cv2

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


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


@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/camera-feed')
def camera_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_frames():
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
