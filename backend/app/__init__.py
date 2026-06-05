import os
from flask import Flask, send_from_directory
from app.config import config_map
from app.extensions import db, migrate, jwt, cors, init_redis

def create_app(config_name=None):
    """Flask application factory."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    init_redis(app)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'recipes'), exist_ok=True)

    # Serve uploaded files (for dev; in production Nginx handles this)
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Register blueprints
    from app.api.v1 import register_blueprints
    register_blueprints(app)

    # Register error handlers
    from app.api.errors import register_error_handlers
    register_error_handlers(app)

    # Start scheduler (only in production or if explicitly enabled)
    if os.getenv('ENABLE_SCHEDULER', 'false').lower() == 'true':
        from app.tasks.scheduler import init_scheduler
        init_scheduler(app)

    # Create tables in development
    if app.config.get('DEBUG'):
        with app.app_context():
            from app.models import user, recipe, community
            db.create_all()

    return app
