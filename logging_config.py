import logging

"""
Module to configure file-based logging for the Flask application.

Logs are written to app.log in a structured format.

"""
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s -%(message)s",
    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
