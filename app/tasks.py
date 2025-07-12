# from app.extensions import collection
# from app.celery_worker import celery

# # from logging_config import logger
# import logging

# # Configure logging for Celery
# logging.basicConfig(
#     level=logging.INFO,
#     format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
#     handlers=[
#         logging.FileHandler("/app/logs/celery.log"),  # Separate log file for Celery
#         logging.StreamHandler(),
#     ],
# )
# logger = logging.getLogger(__name__)


# @celery.task
# def save_event_mongodb(event):
#     logger.info("Saving event to mongodb %s", event)
#     collection.insert_one(event)
#     logger.info("Event Saved Successfully")


from app.extensions import collection
from app.celery_worker import celery
import logging

# Get logger for this module
logger = logging.getLogger(__name__)


@celery.task(bind=True)
def save_event_mongodb(self, event):
    """Save event to MongoDB
    Returns:
        dict: Success response containing:
            - status (str): "success" if operation completed
            - inserted_id (str): MongoDB ObjectId as string

    Raises:
        Exception: Automatically retries on any exception with exponential backoff

    """
    try:
        logger.info("CELERY TASK: Saving event to mongodb %s", event)

        # Insert into MongoDB
        result = collection.insert_one(event)

        logger.info(
            "CELERY TASK: Event saved successfully with ID %s", str(result.inserted_id)
        )

        return {"status": "success", "inserted_id": str(result.inserted_id)}

    except Exception as e:
        logger.error("CELERY TASK: Failed to save event: %s", str(e))

        raise self.retry(exc=e, countdown=60, max_retries=3)
