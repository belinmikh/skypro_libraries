import logging
import os


def create_basic_logger(name: str) -> logging.Logger:
    """Creates basic logger
    Usage in module:
    logger = create_basic_logger(__name__)

    :param name: put __name__ here
    :return: basic logger"""
    name_file = name
    while True:
        if "." in name_file:
            name_file = name_file[: name_file.index(".")].upper() + "_" + name_file[name_file.index(".") + 1:]
        else:
            break

    if not os.path.exists("logs"):
        os.makedirs("logs")

    with open(f"logs/{name_file}.log", "w"):
        pass

    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(f"logs/{name_file}.log")
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s (%(name)s.%(funcName)s): %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    return logger
