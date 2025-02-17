import logging
from logging import Logger

import colorlog


def setup_logging() -> Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.info("Starting crypto app")

    console_handler = colorlog.StreamHandler()
    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s %(name)s:%(lineno)d - %(message)s%(reset)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    console_handler.setFormatter(color_formatter)
    logger.addHandler(console_handler)
    return logger


if __name__ == "__main__":
    main_logger = setup_logging()

    main_logger.debug("Debug message")
    main_logger.info("Info message")
    main_logger.warning("Warning message")
    main_logger.error("Error message")
    main_logger.critical("Critical message")
