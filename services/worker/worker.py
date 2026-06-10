import boto3
import time

QUEUE_URL = "https://sqs.eu-west-1.amazonaws.com/968477812241/cloud-project-queue"

sqs = boto3.client(
    "sqs",
    region_name="eu-west-1"
)

print("Worker iniciado")

while True:

    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )

    messages = response.get("Messages", [])

    for message in messages:

        print("Mensagem recebida:")
        print(message["Body"])

        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=message["ReceiptHandle"]
        )

    time.sleep(5)