import pytest

from src.loggers import create_basic_logger


def test_create_basic_logger() -> None:
    logger = create_basic_logger(__name__)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

    with open("logs/TESTS_test_loggers.log") as file:
        assert file.readline()[26:] == "DEBUG (tests.test_loggers.test_create_basic_logger): Debug message\n"
        assert file.readline()[26:] == "INFO (tests.test_loggers.test_create_basic_logger): Info message\n"
        assert file.readline()[26:] == "WARNING (tests.test_loggers.test_create_basic_logger): Warning message\n"
        assert file.readline()[26:] == "ERROR (tests.test_loggers.test_create_basic_logger): Error message\n"
        assert file.readline()[26:] == "CRITICAL (tests.test_loggers.test_create_basic_logger): Critical message\n"


def test_create_basic_logger_raises() -> None:
    with pytest.raises(TypeError):
        create_basic_logger(123)
