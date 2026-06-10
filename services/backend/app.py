from flask import Flask
import boto3

app = Flask(__name__)

QUEUE_URL = "https://sqs.eu-west-1.amazonaws.com/968477812241/cloud-project-queue"

sqs = boto3.client(
    "sqs",
    region_name="eu-west-1"
)

@app.route("/")
def home():
    return "Backend Running"

@app.route("/api/status")
def status():
    return {
        "status": "running",
        "service": "backend"
    }

@app.route("/send")
def send_message():

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody="Mensagem enviada pelo backend"
    )

    return {
        "message": "Enviado para SQS"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)