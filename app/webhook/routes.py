from flask import request, jsonify, render_template
from . import webhook_bp
from app.extensions import collection
from datetime import datetime, timezone


@webhook_bp.route("/")
def home():
    return render_template("index.html")


@webhook_bp.route("/receiver", methods=["POST"])
def receiver():
    data = request.json
    event = {}

    if "pusher" in data:
        event = {
            "author": data["pusher"]["name"],
            "action": "push",
            "from_branch": None,
            "to_branch": data["ref"].split("/")[-1],
            "timestamp": datetime.now(timezone.utc).isoformat(),
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
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    else:
        return "Event not handled", 400

    collection.insert_one(event)
    return "", 200


@webhook_bp.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find().sort("timestamp", -1))
    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify(events)
