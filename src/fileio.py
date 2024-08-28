import datetime
import json
import os
from functools import wraps
from typing import Any, Callable

import pandas as pd

from src.loggers import create_basic_logger
from src.utils import provide_mode

logger = create_basic_logger(__name__)


def read_xlsx(path: str) -> pd.DataFrame:
    """Makes DataFrame object out of .xlsx

    :param path: .xlsx file path
    :return: DataFrame"""
    if not isinstance(path, str):
        raise TypeError
    if not path.endswith(".xlsx"):
        raise ValueError("Name of file should ends with .xlsx")
    try:
        data = pd.read_excel(path)
        data["Дата операции"] = pd.to_datetime(data["Дата операции"], format='%d.%m.%Y %H:%M:%S')
        data["Дата платежа"] = pd.to_datetime(data["Дата платежа"], format='%d.%m.%Y')
        return data
    except FileNotFoundError:
        logger.error(f"{path} is missing")
        raise FileNotFoundError(f"{path} is missing")
    except Exception as ex:
        logger.error(f"{ex}")
        raise ex


def saves(path: str = "") -> Callable:
    """Decorator, saves func result to .json,
    default path: data/func_YYYY-MM-DD_HH-MM-SS.json

    :param path: .json file path
    :return: decorator"""
    if not isinstance(path, str):
        raise TypeError("File path should be a string")

    def saves_internal(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            res = func(*args, **kwargs)
            if isinstance(res, pd.DataFrame):
                res = provide_mode(res, mode="dict")
            try:
                with open(path, "w") as f:
                    json.dump(res, f)
                logger.info(f"saved {path}")
            except FileNotFoundError:
                now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                if not os.path.exists("data"):
                    os.makedirs("data")
                with open("data/" + func.__name__ + "_" + now + ".json", "w") as f:
                    json.dump(res, f)
                logger.info("saved default")
            return res
        return wrapper
    return saves_internal
