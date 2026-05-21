import logging
from pathlib import Path


def get_logger(
        name: str = "automation"
) -> logging.Logger:

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    # Create logs directory
    log_dir = Path("logs")

    log_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Fixed log file
    log_file = (
        log_dir / "automation.log"
    )

    # File Handler
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    file_handler.setFormatter(
        formatter
    )

    # Console Handler
    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )

    # Add Handlers
    logger.addHandler(
        file_handler
    )

    logger.addHandler(
        console_handler
    )

    logger.propagate = False

    return logger