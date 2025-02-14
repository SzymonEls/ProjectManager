from flask import Flask
from config import Config
from app.extensions import db
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from flask_migrate import upgrade

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask extensions here
    db.init_app(app)
    # Initialize Flask-Migrate here
    migrate = Migrate(app, db)
    if app.config["AUTOMATIC_DB_CREATION"]:
        with app.app_context():
            DB_FILE = "db/app.db"
            if not os.path.exists(DB_FILE):
                db.create_all()
            else:
                upgrade()

    # Initialize Flask-Login here
    login_manager = LoginManager(app)
    login_manager.login_view = 'main.login'  # Redirect to login page if user is not authenticated

    # User loader function for Flask-Login
    from app.main.user import User  # Assuming your User model is in app.models

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.projects import bp as projects_bp
    app.register_blueprint(projects_bp, url_prefix="/projects")

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app