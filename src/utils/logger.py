# src/utils/logger.py

import logging

def setupLogging(level="INFO"):
    """
    Set up a centralized logging configuration.

    :param level: Logging level as a string (e.g., "DEBUG", "INFO").
    :return: None
    """
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=getattr(logging, level.upper(), "INFO"), format=log_format)
    logging.info("Logging initialized.")