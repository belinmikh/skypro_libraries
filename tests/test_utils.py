from typing import Any

import pytest

from src.utils import extract, provide_mode


def test_extract() -> None:

    tale = {
        "Остров Буян": {
            "Дуб 0": None,
            "Дуб 1": "Жёлудь",
            "Дуб 2": {
                "Сундук": {
                    "Заяц": {"Утка": {"Яйцо": {"Игла": "Смерть кощеева"}}},
                    "Бутылка рома": "Смерть (одно и то же)",
                },
                "Сова": "А я думала камера",
            },
            "Дуб 3": "Кот учёный (сказкой ошибся)",
        },
        "Остров Пасхи": {"Статуи": ["Рожа 0", "Рожа 1", "Рожа 2"]},
    }
    # Wrong path testing
    assert (
        extract(
            tale,
            (
                "Остров Буян",
                "Тот берег моря",
                "Хромая блоха",
                "Лужа",
                "Орёл",
                "Птенец",
                "Город",
                "Заяц",
                "Тулуп",
                "Какой заяц?! Какой орёл?!",
            ),
        )
        is None
    )
    # Not full path testing
    assert extract(tale, ("Остров Пасхи",)) == {"Статуи": ["Рожа 0", "Рожа 1", "Рожа 2"]}
    # Full path testing
    assert extract(tale, ("Остров Буян", "Дуб 2", "Сундук", "Заяц", "Утка", "Яйцо", "Игла")) == "Смерть кощеева"


@pytest.mark.parametrize(
    "test_input0, test_input1", [("bimbim", ("ye", "yo")), ({"lol": "kek"}, 123), (321, "bambam")]
)
def test_extract_bad_input(test_input0: Any, test_input1: Any) -> None:
    assert extract(test_input0, test_input1) is None


def test_provide_mode_raises(operations: Any) -> None:
    with pytest.raises(TypeError):
        provide_mode("abobus", mode=123)

    with pytest.raises(ValueError) as ex:
        provide_mode(operations, mode="abobus")

    assert str(ex) == "<ExceptionInfo ValueError('Unknown mode') tblen=2>"
