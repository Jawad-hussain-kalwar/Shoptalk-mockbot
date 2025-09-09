import logging
import os
from logging.handlers import RotatingFileHandler


def init_logging() -> None:
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", "app.log")

    logger = logging.getLogger()
    if any(isinstance(h, RotatingFileHandler) for h in logger.handlers):
        return

    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


