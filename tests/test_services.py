import json

import numpy as np

from src.services import phone_search, search_individuals, simple_search


def test_simple_search(operations, ops_str_search) -> None:
    a = simple_search(operations, "банк", mode="dict")
    b = ops_str_search
    assert a == b


def test_phone_search(operations, ops_phone) -> None:
    assert phone_search(operations, mode="dict") == ops_phone


def test_search_individuals(operations, ops_individuals) -> None:
    assert search_individuals(operations, mode="dict") == ops_individuals
