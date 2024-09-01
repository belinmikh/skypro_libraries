import datetime
from typing import Any
from unittest.mock import patch

import pytest

from src.external_api import convert_currency, get_stocks, stocks_to_rub


@patch("dotenv.load_dotenv")
@patch("os.getenv")
@patch("requests.request")
def test_convert_currency_bad_request(mock_rq: Any, mock_getenv: Any, mock_load_dotenv: Any, al_bad_request) -> None:
    mock_rq.return_value.status_code = 429
    mock_rq.return_value.json.return_value = al_bad_request
    mock_getenv.return_value = "your_key"
    mock_load_dotenv.return_value = None

    headers = {"apikey": "your_key"}
    payload: dict = {}

    assert convert_currency(25.0, "GBP", "JPY", datetime.datetime(2018, 2, 22)) is None

    mock_rq.assert_called_once_with(
        "GET",
        "https://api.apilayer.com/exchangerates_data/convert?to=JPY&from=GBP&amount=25.0&date=2018-02-22",
        headers=headers,
        data=payload,
    )

    with open("logs/SRC_external_api.log", "r", encoding="UTF-8") as f:
        assert f.read().endswith(
            "ERROR (src.external_api.convert_currency): "
            "api.apilayer.com 429 You have exceeded your API rate limit.\n"
        )


@patch("dotenv.load_dotenv")
@patch("os.getenv")
@patch("requests.request")
def test_convert_currency_ok(mock_rq: Any, mock_getenv: Any, mock_load_dotenv: Any, al_ok) -> None:
    mock_rq.return_value.status_code = 200
    mock_rq.return_value.json.return_value = al_ok
    mock_getenv.return_value = "your_key"
    mock_load_dotenv.return_value = None

    headers = {"apikey": "your_key"}
    payload: dict = {}

    assert convert_currency(25.0, "GBP", "JPY", datetime.datetime(2018, 2, 22)) == 3724.305775

    mock_rq.assert_called_once_with(
        "GET",
        "https://api.apilayer.com/exchangerates_data/convert?to=JPY&from=GBP&amount=25.0&date=2018-02-22",
        headers=headers,
        data=payload,
    )

    with open("logs/SRC_external_api.log", "r", encoding="UTF-8") as f:
        assert f.read().endswith(" - INFO (src.external_api.convert_currency): api.apilayer.com 200 ok\n")


def test_convert_currency_raises() -> None:
    with pytest.raises(TypeError):
        convert_currency("ABOBUS", "ABOBUS", "ABOBUS", "ABOBUS")


@patch("dotenv.load_dotenv")
@patch("os.getenv")
@patch("requests.get")
def test_get_stocks_empty(mock_rq: Any, mock_getenv: Any, mock_load_dotenv: Any) -> None:
    mock_getenv.return_value = "your_key"
    mock_load_dotenv.return_value = None

    assert get_stocks() == dict()

    assert not mock_rq.called


@patch("dotenv.load_dotenv")
@patch("os.getenv")
@patch("requests.get")
def test_get_stocks_bad_request(mock_rq: Any, mock_getenv: Any, mock_load_dotenv: Any, ms_bad_request) -> None:
    mock_rq.return_value.status_code = 404
    mock_rq.return_value.json.return_value = ms_bad_request
    mock_getenv.return_value = "your_key"
    mock_load_dotenv.return_value = None

    url = "https://api.marketstack.com/v1/eod?access_key=your_key"

    querystring = {"symbols": "ABOBUS"}

    assert get_stocks("ABOBUS") == dict()

    mock_rq.assert_called_once_with(url, params=querystring)

    with open("logs/SRC_external_api.log", "r", encoding="UTF-8") as f:
        assert f.read().endswith("api.marketstack.com 404 Request failed with validation error\n")


@patch("dotenv.load_dotenv")
@patch("os.getenv")
@patch("requests.get")
def test_get_stocks_ok(mock_rq: Any, mock_getenv: Any, mock_load_dotenv: Any, ms_ok) -> None:
    mock_rq.return_value.status_code = 200
    mock_rq.return_value.json.return_value = ms_ok
    mock_getenv.return_value = "your_key"
    mock_load_dotenv.return_value = None

    url = "https://api.marketstack.com/v1/eod?access_key=your_key"

    querystring = {"symbols": "AAPL"}

    assert get_stocks("AAPL") == {"AAPL": 132.995}

    mock_rq.assert_called_once_with(url, params=querystring)

    with open("logs/SRC_external_api.log", "r", encoding="UTF-8") as f:
        assert f.read().endswith("api.marketstack.com 200 ok\n")


def test_get_stocks_raises() -> None:
    with pytest.raises(TypeError):
        get_stocks(None, 123)


@patch("src.external_api.convert_currency")
def test_stocks_to_rub(mock: Any) -> None:
    mock.return_value = 100.0

    assert stocks_to_rub({"BIMBIM": 0.5, "BAMBAM": 1.5}) == [
        {"stock": "BIMBIM", "price": 50.0},
        {"stock": "BAMBAM", "price": 150.0},
    ]

    mock.assert_called_once_with(1.0, "USD")


@patch("src.external_api.convert_currency")
def test_stocks_to_rub_empty(mock: Any) -> None:
    assert stocks_to_rub(dict()) == []
    assert not mock.called


def test_stocks_to_rub_raises() -> None:
    with pytest.raises(TypeError):
        stocks_to_rub(123)

    with pytest.raises(TypeError) as ex:
        stocks_to_rub({"ABOBUS": "ABOBUS"})

    assert str(ex) == "<ExceptionInfo TypeError('Stocks dict format is unacceptable') tblen=2>"
