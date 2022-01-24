import logging
import logging.config
import sys


def initialise_logger(logging_ini_path):
    # load log file
    logging.config.fileConfig(logging_ini_path)

    # log unhandled exceptions
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.error(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback))

    # register system exception handler
    sys.excepthook = handle_exception
