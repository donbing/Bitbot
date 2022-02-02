from os import path
from src.configuration.bitbot_logging import initialise_logger
import logging
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../config/logging.ini')

initialise_logger(log_file_path)

logging.debug('log test')

