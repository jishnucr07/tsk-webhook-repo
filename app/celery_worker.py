from celery import Celery

from celery.signals import setup_logging
import logging
import os

celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)


@setup_logging.connect
def config_loggers(*args, **kwargs):
    """Configure logging when Celery worker starts"""
    # Ensure logs directory exists
    os.makedirs("/app/logs", exist_ok=True)

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - CELERY - %(name)s - %(message)s",
        handlers=[logging.FileHandler("/app/logs/celery.log"), logging.StreamHandler()],
        force=True,  # Force reconfiguration
    )
