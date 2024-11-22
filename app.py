from flask import Flask, render_template, Response, request, abort
from flask_cors import CORS
from config import Config
from models import db, User
from api.user_route import user_bp
from api.mfa_route import mfa_bp
from api.camera_route import camera_bp

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
db.init_app(app)

CORS(app, resources={r"/api/*": {
    "origins":Config.CORS_ORIGINS.split(","),
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True,
    "max_age": 3600
    }})

app.register_blueprint(user_bp)
app.register_blueprint(mfa_bp)
app.register_blueprint(camera_bp)

@app.before_request
def check_ip_access():
    client_ip = request.remote_addr
    blacklist = Config.IP_BLACKLIST

    if client_ip in blacklist:
        app.logger.warning(f"Blocked access from blacklisted IP: {client_ip}")
        abort(403, description="Access denied")

@app.before_request
def validate_referer():
    referer = request.headers.get("Referer")
    allowed_referers = Config.CORS_ORIGINS
    if referer and not any(referer.startswith(origin) for origin in allowed_referers):
        abort(403, description="Forbidden: Invalid Referer")

@app.after_request
def add_header(response):
    response.headers['X-Robots-Tag'] = 'noindex, nofollow'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
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
