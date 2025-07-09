import os
from flask import Flask

# from app.webhook.routes import webhook
from app.webhook import webhook_bp


# Creating our flask app
def create_app():
    template_path = os.path.join(os.path.dirname(__file__), "webhook", "templates")

    app = Flask(__name__, template_folder=template_path)

    # registering all the blueprints
    app.register_blueprint(webhook_bp, url_prefix="/")

    return app
