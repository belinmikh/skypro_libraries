from typing import Any, Literal

import numpy as np
import pandas as pd


def extract(dictionary: dict, _path: tuple) -> Any:
    """Tries to get nested in dict data, None otherwise

    :param dictionary: dict
    :param _path: tuple of anything that could be keys
    :return: value at path"""
    if not isinstance(dictionary, dict):
        return None
    if not isinstance(_path, tuple):
        return None
    for p in _path:
        if p not in dictionary.keys():
            return None
        if isinstance(dictionary[p], dict) and len(_path) > 1:
            return extract(dictionary[p], tuple(_path[1:]))
        else:
            return dictionary[p]


def provide_mode(data: pd.DataFrame, mode: Literal["dataframe", "json", "dict"]) -> pd.DataFrame | dict | str:
    """Provides output mode for functions that are working with dataframes

    :param data: DataFrame object
    :param mode: output mode (dataframe, json, dict)"""
    if not isinstance(mode, str) or not isinstance(data, pd.DataFrame):
        raise TypeError
    if mode == "dataframe":
        return data
    elif mode == "json":
        # replacing datetime with original formatted strings
        data["Дата операции"] = data["Дата операции"].dt.strftime("%d.%m.%Y %H:%M:%S")
        data["Дата платежа"] = data["Дата платежа"].dt.strftime("%d.%m.%Y")
        return data.replace({np.nan: None}).to_json(orient="records")
    elif mode == "dict":
        # replacing datetime with original formatted strings
        # because I don't want to see Timestamps in dict
        data["Дата операции"] = data["Дата операции"].dt.strftime("%d.%m.%Y %H:%M:%S")
        data["Дата платежа"] = data["Дата платежа"].dt.strftime("%d.%m.%Y")
        return data.replace({np.nan: None}).to_dict(orient="records")
    else:
        raise ValueError("Unknown mode")
