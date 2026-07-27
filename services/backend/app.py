from flask import Flask, request, jsonify
import boto3
import json
import os
from datetime import datetime, timezone

app = Flask(__name__)

AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")
QUEUE_URL = os.getenv(
    "SQS_QUEUE_URL",
    "https://sqs.eu-west-1.amazonaws.com/968477812241/cloud-project-queue"
)

sqs = boto3.client(
    "sqs",
    region_name=AWS_REGION
)


@app.route("/")
def home():
    return jsonify({
        "service": "ingest-api",
        "status": "running"
    })


@app.route("/api/status")
def status():
    return jsonify({
        "status": "running",
        "service": "ingest-api"
    })


@app.route("/telemetry", methods=["POST"])
def send_telemetry():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    required_fields = ["deviceId", "temperature", "humidity"]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing_fields
        }), 400

    telemetry = {
        "deviceId": data["deviceId"],
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(telemetry)
    )

    return jsonify({
        "status": "accepted",
        "message": "Telemetry queued for processing",
        "messageId": response["MessageId"],
        "telemetry": telemetry
    }), 202


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)