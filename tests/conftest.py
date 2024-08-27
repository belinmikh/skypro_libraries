import pytest

@pytest.fixture
def al_bad_request() -> dict:
    return {"message": "You have exceeded your API rate limit."}


@pytest.fixture
def al_ok() -> dict:
    return {
        "date": "2018-02-22",
        "historical": "",
        "info": {"rate": 148.972231, "timestamp": 1519328414},
        "query": {"amount": 25.0, "from": "GBP", "to": "JPY"},
        "result": 3724.305775,
        "success": True,
    }


@pytest.fixture
def ms_bad_request() -> dict:
    return {
        "error": {
            "code": "validation_error",
            "message": "Request failed with validation error",
            "context": {"symbols": [{"key": "missing_symbols", "message": "You did not specify any symbols."}]},
        }
    }


@pytest.fixture
def ms_ok() -> dict:
    return {
        "pagination": {"limit": 100, "offset": 0, "count": 100, "total": 9944},
        "data": [
            {
                "open": 129.8,
                "high": 133.04,
                "low": 129.47,
                "close": 132.995,
                "volume": 106686703.0,
                "adj_high": 133.04,
                "adj_low": 129.47,
                "adj_close": 132.995,
                "adj_open": 129.8,
                "adj_volume": 106686703.0,
                "split_factor": 1.0,
                "dividend": 0.0,
                "symbol": "AAPL",
                "exchange": "XNAS",
                "date": "2021-04-09T00:00:00+0000",
            },
        ],
    }