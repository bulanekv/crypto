import os
from typing import List

import requests
from fastapi import (
    APIRouter,
    BackgroundTasks,
    HTTPException,
    status,
)

from ..models.currencyModel import CurrencyInput, CurrencyItem
from .currencydb import (
    add_currency,
    delete_currency,
    get_currencies,
    get_currency,
    update_currency,
)

router = APIRouter()


@router.post("/", status_code=201)
async def post_currency_route(currency: CurrencyInput, background_tasks: BackgroundTasks):
    res = add_currency(currency)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is unavailable",
        )
    elif not res:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Currency symbol already exists",
        )
    else:
        background_tasks.add_task(process_currency, currency.id)
        return True


@router.get("/", response_model=List[CurrencyItem])
async def get_currencies_route():
    items = get_currencies()
    currencies = []
    for item in items:
        currency = CurrencyItem(
            id=item["id"],
            symbol=item.get("symbol", ""),
            name=item.get("name", ""),
            meta=item.get("meta", ""),
        )
        currencies.append(currency)
    return currencies


@router.get("/{id}", response_model=CurrencyItem)
async def get_currency_route(id: str):
    currency = get_currency(id)
    if not currency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found"
        )
    return currency


@router.delete("/{id}")
async def delete_currency_route(id: str):
    currency = get_currency(id)
    if not currency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found"
        )
    res = delete_currency(id)
    if res is None or not res:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is unavailable",
        )
    else:
        return True


# get currency by id
async def process_currency(currency_id: str) -> None:
    url = "https://api.coingecko.com/api/v3/coins/{id}".format(id=currency_id)

    headers = {
        "accept": "application/json",
        "x-cg-pro-api-key": os.getenv("COINGECKO_API_KEY"),
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        update_currency(currency_id, response.json())
    elif response.status_code == 400:
        if response.json().get("error_code") == 10010:
            delete_currency(currency_id)
