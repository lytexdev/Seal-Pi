# List of blueprints to be registered with their prefixes
blueprints = [
    (camera_bp, "/camera"),
]

# List of routes/endpoints that require login
require_login_endpoints = [
    "camera"
]

# List of routes without login
allowed_endpoints = []

def register_blueprints(app):
    """Register all blueprints listed in the blueprints variable."""
    for blueprint, prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=prefix)

    register_custom_modules(app)
