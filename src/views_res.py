import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

from src.loggers import create_basic_logger

logger = create_basic_logger(__name__)


def greetings(date: str | None = None) -> str:
    if date:
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except Exception as ex:
            logger.error(f'Caught {ex}')
            raise ex
    else:
        date = datetime.datetime.now()
    h = date.hour
    if h <= 6:
        return 'Доброй ночи'
    elif h <= 12:
        return 'Доброе утро'
    elif h <= 18:
        return 'Добрый день'
    else:
        return 'Добрый вечер'


def cards_stats(data: pd.DataFrame, date: str | None = None) -> list[dict]:
    # I sure there is a way to do it with pandas methods, but
    # at least for now I'm doing it my way
    if date:
        date = pd.to_datetime(date, format='%Y-%m-%d %H:%M:%S')
    else:
        date = pd.to_datetime(datetime.datetime.now())
    begin = date + relativedelta(months=-1)
    to_return = dict()
    # data["Дата операции"] = data["Дата операции"].fillna(
    #     pd.to_datetime('0001-01-01 00:00:01', format='%Y-%m-%d %H:%M:%S')
    #  )
    # data = data.loc[begin <= data["Дата операции"].dt. <= date]
    data = data.loc[(begin <= data["Дата операции"]) & (data["Дата операции"] <= date)]
    data = data.reset_index()  # make sure indexes pair with number of rows
    for i, row in data.iterrows():
        if not isinstance(row["Номер карты"], str):
            continue
        if row["Номер карты"] not in to_return.keys():
            to_return.update(
                {row["Номер карты"]:
                     {
                         "total_spent": 0,
                         "cashback": 0
                     }
                }
            )

        # "Сумма платежа" is negative if it is a spending
        if isinstance(row["Сумма платежа"], float) and row["Сумма платежа"] < 0:
            to_return[row["Номер карты"]]["total_spent"] -= row["Сумма платежа"]

        if isinstance(row["Кэшбэк"], float) and row["Кэшбэк"] > 0:
            to_return[row["Номер карты"]]["cashback"] += row["Кэшбэк"]
    to_return_reformatted = []
    for card, info in to_return.items():
        to_return_reformatted.append(
            {
                "last_digits": card[1:],
                "total_spent": round(info["total_spent"], 2),
                "cashback": round(info["cashback"], 2)
            }
        )
    return to_return_reformatted


def top_transactions(data: pd.DataFrame, n: int = 5, date: str | None = None) -> list[dict]:
    if date:
        date = pd.to_datetime(date, format='%Y-%m-%d %H:%M:%S')
    else:
        date = pd.to_datetime(datetime.datetime.now())
    begin = date + relativedelta(months=-1)
    data = data.loc[(begin <= data["Дата операции"]) & (data["Дата операции"] <= date)]
    data = data.sort_values("Сумма операции с округлением", ascending=False)
    data = data.reset_index()  # make sure indexes pair with number of rows
    to_return = []
    for i, row in data.iterrows():
        try:
            item_date = row["Дата платежа"].strftime('%d.%m.%Y')
        except:
            item_date = None
        to_return.append(
            {
                "date": item_date,
                "amount": row["Сумма операции с округлением"],
                "category": row["Категория"],
                "description": row["Описание"]
            }
        )
        if len(to_return) >= n:
            break
    return to_return
