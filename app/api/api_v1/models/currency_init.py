import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from app.settings import settings

load_dotenv()

stage = os.getenv("STAGE", "PRD")
test_stage = os.getenv("TEST", None)

print(stage)
print(test_stage)

table_name = settings.table_name
if test_stage:
    table_name = table_name + "_test"
if stage == "DEV" or stage == "TEST":
    dynamodb = boto3.resource(
        "dynamodb", endpoint_url=os.getenv('DYNAMODB_ENDPOINT', 'http://localhost:8000'), region_name="eu-central-1"
    )
    dynamo_client = boto3.client(
        "dynamodb", endpoint_url=os.getenv('DYNAMODB_ENDPOINT', 'http://localhost:8000'), region_name="eu-central-1"
    )
else:
    session = boto3.Session(region_name="eu-central-1")
    dynamodb = session.resource("dynamodb")
    dynamo_client = session.client("dynamodb")


def create_table():
    global table_name
    try:
        _ = dynamo_client.describe_table(TableName=table_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            _ = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
                ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
            )


def remove_table():
    try:
        _ = dynamo_client.delete_table(TableName=table_name)
    except ClientError:
        pass
