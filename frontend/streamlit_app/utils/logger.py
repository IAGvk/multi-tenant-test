import logging
from logging.handlers import RotatingFileHandler

def get_logger(name: str, log_file: str = "app.log", level: int = logging.DEBUG) -> logging.Logger:
    """
    Creates and configures a logger with a rotating file handler and console output.

    Args:
        name (str): Name of the logger (usually __name__).
        log_file (str): Path to the log file.
        level (int): Logging level (e.g., logging.DEBUG, logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate log handlers
    if not logger.hasHandlers():
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)

        # Rotating file handler
        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger