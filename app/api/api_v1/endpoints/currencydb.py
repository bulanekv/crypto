import json
import os

import boto3
from dotenv import load_dotenv

from app.api.api_v1.models.currencyModel import CurrencyInput
from app.settings import settings

load_dotenv()

stage = os.getenv("STAGE", "PRD")
test_stage = os.getenv("TEST", None)

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


def get_currency(id: str) -> dict | None:
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            "id": id,
        }
    )
    if "Item" not in response:
        return None
    return response["Item"]


def get_currencies() -> list | None:
    table = dynamodb.Table(table_name)
    response = table.scan()
    if "Items" not in response:
        return None
    return response.get("Items", [])


def add_currency(currency: CurrencyInput) -> bool | None:
    if get_currency(currency.id) is None:
        table = dynamodb.Table(table_name)
        response = table.put_item(
            Item={
                "id": currency.id,
            }
        )
        if "ResponseMetadata" not in response:
            return None
        return response["ResponseMetadata"]["HTTPStatusCode"] == 200
    else:
        return False


def delete_currency(id: str) -> bool | None:
    table = dynamodb.Table(table_name)
    response = table.delete_item(Key={"id": id})
    if "ResponseMetadata" not in response:
        return None
    return response["ResponseMetadata"]["HTTPStatusCode"] == 200


def update_currency(currency_id: str, data: dict) -> None:
    symbol = data.get("symbol", "")
    name = data.get("name", "")
    data.pop("symbol", None)
    data.pop("name", None)
    data.pop("id", None)
    table = dynamodb.Table(table_name)
    _ = table.put_item(
        Item={
            "id": currency_id,
            "symbol": symbol,
            "name": name,
            "meta": json.dumps(data),
        }
    )
