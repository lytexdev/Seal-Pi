from flask import Flask, render_template, Response
from config import Config
from models import db, User
from api.user_route import user_bp
from api.mfa_route import mfa_bp
from api.camera_route import camera_bp

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(mfa_bp)
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
        create_example_admin()
        app.logger.info("Database initialized")

def create_example_admin():
    admin_user = User.query.filter_by(is_admin=True).first()

    if not admin_user:
        admin_user = User(username='admin', email='admin@example.com', is_admin=True)
        admin_user.set_password('admin')
        db.session.add(admin_user)
        db.session.commit()
        app.logger.info("Example Admin user created, please change the default password!")

init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
