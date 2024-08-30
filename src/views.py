import datetime
import json

from src.external_api import convert_currency, stocks_to_rub, get_stocks
from src.fileio import read_xlsx
from src.utils import extract
from src.views_res import greetings, cards_stats, top_transactions


def main_page(date: str | None = None) -> str:
    if date is None:
        dt = datetime.datetime.now()
        date = dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    with open('user_settings.json', encoding='UTF-8') as f:
        user_settings = json.load(f)

    ops = read_xlsx('operations.xlsx')

    response = {
        "greeting": greetings(date),
        "cards": cards_stats(ops, date),
        "top_transactions": top_transactions(ops, 5, date),
        "currency_rates": [
            {
                "currency": cur,
                "rate": convert_currency(1.0, cur, "RUB", dt)
            }
            for cur in extract(user_settings, ("user_currencies",))
        ],
        "stock_prices": stocks_to_rub(
            get_stocks(*extract(user_settings, ("user_stocks",)))
        )
    }

    return json.dumps(response)
