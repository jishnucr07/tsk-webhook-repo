from flask import request, jsonify, render_template
from . import webhook_bp
from app.extensions import collection
from datetime import datetime, timezone, timedelta
from app.tasks import save_event_mongodb
from logging_config import logger


@webhook_bp.route("/")
def home():
    return render_template("index.html")


@webhook_bp.route("/receiver", methods=["POST"])
def receiver():
    """
    Receives webhook events from GitHub and extracts relevant data.

    Supported events:
    - Push: Extracts pusher name and target branch.
    - Pull Request Events: Extracts author, source/target branches, and handles
      both regular PR events and merge events (closed + merged)


    Returns:
        tuple: JSON response with status and HTTP status code
            - 200: {"status": "success"} - Event processed successfully
            - 400: "Event not handled" - Unsupported event type
            - 500: {"status": "error", "task_id": str} - Processing error

    Raises:
        Exception: Logs error and returns 500 response if processing fails
    """
    task = None
    try:
        data = request.json
        logger.info("Received webhook data: %s", data)
        event = {}

        if "pusher" in data:
            event = {
                "author": data["pusher"]["name"],
                "action": "push",
                "from_branch": None,
                "to_branch": data["ref"].split("/")[-1],
                "timestamp": datetime.now(timezone.utc),
            }

        elif "pull_request" in data:
            pr = data["pull_request"]
            action_type = (
                "merge"
                if data["action"] == "closed" and pr.get("merged")
                else "pull_request"
            )
            event = {
                "author": pr["user"]["login"],
                "action": action_type,
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": datetime.now(timezone.utc),
            }

        else:
            return "Event not handled", 400

        task = save_event_mongodb.delay(event)
        logger.info(
            "Queued the task to store(celery) %s event from %s",
            event["action"],
            event["author"],
        )

        return jsonify({"status": "success"}), 200

    except Exception as e:
        logger.error("Error in Webhook /receiver :%s", str(e))
        # Only include task_id if task exists
        response_data = {"status": "error"}
        if task:
            response_data["task_id"] = task.id
        return jsonify(response_data), 500


@webhook_bp.route("/events", methods=["GET"])
def get_events():
    """
     Retrieves recent webhook events from MongoDB.

    Fetches all webhook events stored in the database within the last 15 seconds
    sorted by timestamp in descending order (newest first).


    Returns:
       tuple: JSON response with status and HTTP status code
            - 200: Success response with events array
            - 500: Error response with error message

    Raises:
        Exception: Database connection or query errors are caught and logged
    """

    try:
        time_threshold = datetime.now(timezone.utc) - timedelta(seconds=2200)

        events = list(
            collection.find({"timestamp": {"$gte": time_threshold}}).sort(
                "timestamp", -1
            )
        )
        for e in events:
            e["_id"] = str(e["_id"])
        return jsonify({"status": "success", "events": events})
    except Exception as e:
        logger.error("Error in get_events : %s", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
