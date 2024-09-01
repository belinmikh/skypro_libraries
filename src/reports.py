import datetime
import re
from typing import Literal, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.fileio import saves
from src.utils import provide_mode


@saves()
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: Optional[str] = None,
    mode: Literal["dataframe", "json", "dict"] = "dataframe",
) -> pd.DataFrame | str | dict:
    """Returns filtered by category operations
    in three months before date (default: today)

    :param transactions: DataFrame
    :param category: name of category
    :param date: any comparable with pd.to_datetime string, 'YYYY-MM-DD' for example (default: today)
    :param mode: 'dataframe', 'json', 'dict'
    :return: filtered dataframe in chosen mode
    """
    if date is None:
        date = datetime.datetime.now()
    date = pd.to_datetime(date)
    begin = date + relativedelta(months=-3)
    # using re.escape just in case somebody puts special symbols to search
    transactions = transactions[transactions["Категория"].str.contains(re.escape(category), regex=True, na=False)]
    transactions = transactions.loc[(begin <= transactions["Дата операции"]) & (transactions["Дата операции"] <= date)]
    return provide_mode(transactions, mode=mode)
