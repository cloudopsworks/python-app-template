from flask import Flask

def create_app():
    # Create and configure the Flask application
    app = Flask(__name__)

    # Import and register routes from app/routes.py
    from .routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
