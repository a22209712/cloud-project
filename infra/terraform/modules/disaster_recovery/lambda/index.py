import boto3
import os

PRIMARY_INSTANCE = os.environ["PRIMARY_INSTANCE_ID"]
STANDBY_INSTANCE = os.environ["STANDBY_INSTANCE_ID"]
PRIMARY_REGION = os.environ["PRIMARY_REGION"]
STANDBY_REGION = os.environ["STANDBY_REGION"]

primary = boto3.client("ec2", region_name=PRIMARY_REGION)
standby = boto3.client("ec2", region_name=STANDBY_REGION)


def lambda_handler(event, context):

    response = primary.describe_instances(
        InstanceIds=[PRIMARY_INSTANCE]
    )

    state = response["Reservations"][0]["Instances"][0]["State"]["Name"]

    print(f"Primary instance state: {state}")

    if state != "running":
        standby.start_instances(
            InstanceIds=[STANDBY_INSTANCE]
        )

        print("Standby instance started")

        return {
            "statusCode": 200,
            "message": "Standby started"
        }

    return {
        "statusCode": 200,
        "message": "Primary healthy"
    }