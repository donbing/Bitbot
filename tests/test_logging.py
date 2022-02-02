from os import path
from src.configuration.bitbot_logging import initialise_logger
import logging

current_path = path.dirname(path.abspath(__file__))
log_file_path = path.join(current_path, '../config/logging.ini')
initialise_logger(log_file_path)
logging.debug('log test')
