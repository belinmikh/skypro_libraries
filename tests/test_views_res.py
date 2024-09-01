import pytest

from src.views_res import cards_stats, greetings, top_transactions


def test_greetings() -> None:
    with pytest.raises(ValueError):
        assert greetings("ABOBUS")
    assert greetings("2020-02-02 10:20:30") == "Доброе утро"
    assert greetings("2020-02-02 14:20:30") == "Добрый день"
    assert greetings("2020-02-02 19:12:32") == "Добрый вечер"
    assert greetings("2020-02-03 01:02:03") == "Доброй ночи"


def test_cards_stats(operations) -> None:
    assert cards_stats(operations, "2021-12-20 10:00:00") == [
        {"last_digits": "5091", "total_spent": 55.41, "cashback": 0},
        {"last_digits": "7197", "total_spent": 3756.24, "cashback": 0},
    ]


def test_top_transactions(operations) -> None:
    assert top_transactions(operations, 5, "2021-12-20 10:00:00") == [
        {"date": "16.12.2021", "amount": 14216.42, "category": "ЖКХ", "description": "ЖКУ Квартира"},
        {"date": "16.12.2021", "amount": 1150.0, "category": "Дом и ремонт", "description": "Ofisnaya mebel"},
        {"date": "18.12.2021", "amount": 829.0, "category": "Супермаркеты", "description": "Лента"},
        {"date": "17.12.2021", "amount": 495.0, "category": "Услуги банка", "description": "Плата за обслуживание"},
        {"date": "16.12.2021", "amount": 453.0, "category": "Бонусы", "description": "Кэшбэк за обычные покупки"},
    ]
