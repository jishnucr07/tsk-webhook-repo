import os
from flask import Flask

# from app.webhook.routes import webhook
from app.webhook import webhook_bp


# Creating our flask app
def create_app():
    """
    Create and configure a Flask application instance.

    Template Configuration:
        Sets the template folder to the webhook module's templates directory
        to ensure proper template resolution for the webhook blueprint.

    Blueprint Registration:
        - webhook_bp: Registered at root path ("/") for main application routes


    Returns:
        Flask: Configured Flask application instance ready for use

    """

    # Configure template directory path
    template_path = os.path.join(os.path.dirname(__file__), "webhook", "templates")

    # Create Flask application instance
    app = Flask(__name__, template_folder=template_path)

    # registering all the blueprints
    app.register_blueprint(webhook_bp, url_prefix="/")

    return app
