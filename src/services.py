import re
from typing import Literal

import pandas as pd

from src.loggers import create_basic_logger
from src.utils import provide_mode

logger = create_basic_logger(__name__)


def simple_search(
    data: pd.DataFrame, pat: str, mode: Literal["dataframe", "json", "dict"] = "dataframe"
) -> pd.DataFrame | str | dict:
    """Returns records with substring in 'Описание' or 'Категория' keys

    :param data: DataFrame object
    :param pat: substring search to
    :param mode: 'dataframe', 'json', 'dict'
    :return: filtered dataframe in chosen mode
    """
    if mode not in ["dataframe", "json", "dict"]:
        logger.error(f"called with unknown mode ({mode})")
        raise ValueError("Unknown mode")
    logger.info(f'called with "{pat}" in {mode} mode')
    # using re.escape just in case somebody puts special symbols to search
    desc = data[data["Описание"].str.contains(re.escape(pat), regex=True, na=False)]
    cat = data[data["Категория"].str.contains(re.escape(pat), regex=True, na=False)]
    data = pd.concat([desc, cat])
    return provide_mode(data, mode=mode)


def phone_search(
    data: pd.DataFrame, mode: Literal["dataframe", "json", "dict"] = "dataframe"
) -> pd.DataFrame | str | dict:
    """Returns records with phone number in 'Описание' key

    :param data: DataFrame object
    :param mode: 'dataframe', 'json', 'dict'
    :return: filtered dataframe in chosen mode
    """
    if mode not in ["dataframe", "json", "dict"]:
        logger.error(f"called with unknown mode ({mode})")
        raise ValueError("Unknown mode")
    logger.info(f"called in {mode} mode")
    data = data[data["Описание"].str.contains(r"\+7.\d{3}.\d{3}-\d{2}-\d{2}", regex=True, na=False)]
    return provide_mode(data, mode=mode)


def search_individuals(
    data: pd.DataFrame, mode: Literal["dataframe", "json", "dict"] = "dataframe"
) -> pd.DataFrame | str | dict:
    """

    :param data:
    :param mode:
    :return:
    """
    if mode not in ["dataframe", "json", "dict"]:
        logger.error(f"called with unknown mode ({mode})")
        raise ValueError("Unknown mode")
    logger.info(f"called in {mode} mode")
    data = data.loc[data["Категория"] == "Переводы"]
    data = data[data["Описание"].str.contains(r"[А-Я][а-я]+.[А-Я]\.", regex=True, na=False)]
    return provide_mode(data, mode=mode)
