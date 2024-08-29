import datetime
import os

import requests
from dotenv import load_dotenv

from src.loggers import create_basic_logger
from src.utils import extract

logger = create_basic_logger(__name__)

load_dotenv()


def convert_currency(
    amount: float, currency: str, to: str = "RUB", date: datetime.datetime = datetime.datetime.now()
) -> float | None:
    """Converts currencies

    :param amount: amount, float
    :param currency: currency code ('USD' as example)
    :param to: currency convert to ('RUB' as default)
    :param date: datetime object, today for default
    :return: amount (None if fails)"""
    if not isinstance(amount, float) or not isinstance(currency, str) or not isinstance(date, datetime.datetime):
        raise TypeError

    if amount == 0.0:
        return 0.0

    al_key = os.getenv("AL_KEY")

    headers = {"apikey": al_key}
    payload: dict = {}

    date = date.strftime("%Y-%m-%d")

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to}&from={currency}&amount={amount}&date={date}"

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        logger.info("api.apilayer.com 200 ok")
        result = response.json()
        res = extract(result, ("result",))
        if isinstance(res, float):
            return res
    else:
        logger.error(f"api.apilayer.com {response.status_code} " f'{extract(response.json(), ("message",))}')
    return None


def get_stocks(*args: str) -> dict:
    """Gets stocks last adjusted closing exchange rates in USD

    :param args: stocks' symbols
    :return: {symbol: amount} formatted dict"""
    if len(args) == 0:
        # traffic economy
        return dict()

    for arg in args:
        if not isinstance(arg, str):
            raise TypeError

    ms_key = os.getenv("MS_KEY")

    url = f"https://api.marketstack.com/v1/eod?access_key={ms_key}"

    querystring = {"symbols": ",".join(args)}

    response = requests.get(url, params=querystring)

    to_return = dict()

    if response.status_code == 200:
        logger.info("api.marketstack.com 200 ok")
        result = extract(response.json(), ("data",))
        if isinstance(result, list):
            for rec in result:
                to_return.update({extract(rec, ("symbol",)): extract(rec, ("adj_close",))})
    else:
        logger.info(
            f"api.marketstack.com {response.status_code} " f'{extract(response.json(), ("error", "message", ))}'
        )
    return to_return


def stocks_to_rub(stocks: dict) -> list[dict] | None:
    """Converts stocks exchange rates to RUB

    :param stocks: {stock: amount(USD)} formatted dict
    :return: {stock: amount(RUB)} formatted dict"""
    if not isinstance(stocks, dict):
        raise TypeError

    for k, v in stocks.items():
        if not isinstance(k, str) or not isinstance(v, float):
            raise TypeError("Stocks dict format is unacceptable")

    if len(stocks) == 0:
        return []

    # traffic economy (calling just once)
    exchange = convert_currency(1.0, "USD")
    if not exchange:
        return None

    # to_return = dict()
    to_return = []
    for sym in stocks.keys():
        to_return.append(
            {
                "stock": sym,
                "price": round(stocks[sym] * exchange, 2)
            }
        )
        # to_return.update({sym: round(stocks[sym] * exchange, 2)})
    return to_return
