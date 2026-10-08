import logging
from pathlib import Path

def configure_logging() -> logging.Logger:
    Path("logs").mkdir(exist_ok=True)
    logger = logging.getLogger("wealth_advisor")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    stream = logging.StreamHandler()
    stream.setFormatter(fmt)
    file_handler = logging.FileHandler("logs/wealth_advisor.log")
    file_handler.setFormatter(fmt)
    logger.addHandler(stream)
    logger.addHandler(file_handler)
    return logger
