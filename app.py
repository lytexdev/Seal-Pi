from flask import Flask, render_template, Response
from config import Config
from models import db
from api.user_route import user_bp
from api.camera_route import camera_bp

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(camera_bp)


@app.after_request
def add_header(response):
    response.headers['X-Robots-Tag'] = 'noindex, nofollow'
    return response

@app.route('/robots.txt')
def robots_txt():
    return Response("User-agent: *\nDisallow: /", mimetype="text/plain")

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
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
