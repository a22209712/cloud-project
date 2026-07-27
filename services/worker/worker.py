import boto3
import json
import os
import time
import psycopg2

AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")

QUEUE_URL = os.getenv(
    "SQS_QUEUE_URL",
    "https://sqs.eu-west-1.amazonaws.com/968477812241/cloud-project-queue"
)

DB_HOST = os.getenv(
    "DB_HOST",
    "cloud-project-postgres.c9mga6m2u5sk.eu-west-1.rds.amazonaws.com"
)

DB_NAME = os.getenv("DB_NAME", "telemetry")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

SECRET_ARN = os.getenv(
    "DB_SECRET_ARN",
    "arn:aws:secretsmanager:eu-west-1:968477812241:secret:rds!db-5c654c97-31e2-4a3b-9ee0-c19feae81097-x4Vlx7"
)

sqs = boto3.client("sqs", region_name=AWS_REGION)
secretsmanager = boto3.client("secretsmanager", region_name=AWS_REGION)


def get_database_credentials():
    response = secretsmanager.get_secret_value(
        SecretId=SECRET_ARN
    )

    secret = json.loads(response["SecretString"])

    return secret["username"], secret["password"]


def get_database_connection():
    username, password = get_database_credentials()

    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=username,
        password=password,
        connect_timeout=10
    )


def create_table_if_not_exists():
    connection = get_database_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_readings (
                    id SERIAL PRIMARY KEY,
                    device_id VARCHAR(100) NOT NULL,
                    temperature DOUBLE PRECISION NOT NULL,
                    humidity DOUBLE PRECISION NOT NULL,
                    recorded_at TIMESTAMPTZ NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                )
            """)

        connection.commit()
        print("Database table ready.")

    finally:
        connection.close()


def save_telemetry(telemetry):
    connection = get_database_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO telemetry_readings (
                    device_id,
                    temperature,
                    humidity,
                    recorded_at
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    telemetry["deviceId"],
                    telemetry["temperature"],
                    telemetry["humidity"],
                    telemetry["timestamp"]
                )
            )

        connection.commit()

    finally:
        connection.close()


def process_message(message):
    telemetry = json.loads(message["Body"])

    required_fields = [
        "deviceId",
        "temperature",
        "humidity",
        "timestamp"
    ]

    for field in required_fields:
        if field not in telemetry:
            raise ValueError(f"Missing required field: {field}")

    print()
    print("Telemetry received:")
    print(f"Device: {telemetry['deviceId']}")
    print(f"Temperature: {telemetry['temperature']} °C")
    print(f"Humidity: {telemetry['humidity']} %")
    print(f"Timestamp: {telemetry['timestamp']}")

    save_telemetry(telemetry)

    print("Telemetry saved successfully to PostgreSQL.")


def main():
    print("Worker service started")
    print(f"Listening to queue: {QUEUE_URL}")

    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10,
                AttributeNames=["ApproximateReceiveCount"]
            )

            messages = response.get("Messages", [])

            for message in messages:
                try:
                    receive_count = message.get(
                        "Attributes", {}
                    ).get("ApproximateReceiveCount", "unknown")

                    print(f"Processing attempt: {receive_count}")

                    process_message(message)

                    sqs.delete_message(
                        QueueUrl=QUEUE_URL,
                        ReceiptHandle=message["ReceiptHandle"]
                    )

                    print("Message deleted from SQS after successful processing.")

                except Exception as error:
                    print(f"Error processing message: {error}")
                    print(
                        "Message was NOT deleted. "
                        "It will be retried and eventually sent to the DLQ."
                    )

        except Exception as error:
            print(f"Worker error: {error}")
            time.sleep(5)


if __name__ == "__main__":
    try:
        create_table_if_not_exists()
        main()
    except Exception as error:
        print(f"Worker startup failed: {error}")
        raise