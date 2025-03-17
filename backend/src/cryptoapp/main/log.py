import json
import logging
from logging.config import dictConfig
from pathlib import Path
from typing import Any


def parse_logging_config(path: str | Path | None = None) -> dict[str, Any]:
    if path is None:
        current_dir = Path(__file__).resolve().parent
        config_path = current_dir / "logging.json"
    else:
        config_path = Path(path).resolve()

    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)
    return config  # type: ignore


def setup_logging() -> None:
    config = parse_logging_config()
    dictConfig(config)


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
