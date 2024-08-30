from typing import Any

from src.reports import spending_by_category


def test_spending_by_category(operations: Any) -> None:
    assert spending_by_category(operations, "Переводы", "2021-12-20", mode="dict") == [
        {
            "Дата операции": "19.12.2021 18:38:09",
            "Дата платежа": "19.12.2021",
            "Номер карты": None,
            "Статус": "OK",
            "Сумма операции": -186.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -186.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Переводы",
            "MCC": None,
            "Описание": "Андрей Х.",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 186.0,
        },
        {
            "Дата операции": "18.12.2021 17:21:34",
            "Дата платежа": "18.12.2021",
            "Номер карты": None,
            "Статус": "OK",
            "Сумма операции": -200.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -200.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Переводы",
            "MCC": None,
            "Описание": "Андрей Х.",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 200.0,
        },
    ]
