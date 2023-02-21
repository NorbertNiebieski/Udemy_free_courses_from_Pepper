import logging.handlers
import os
from datetime import datetime

is_printing = True
_log_folder = "log\\"
_log_level_from_environment = "DEBUG"


def _prepare_folder_file_and_path(folder_path):
    log_path = folder_path + str(datetime.now()).replace(" ", "_", 10).replace(":", "-")[:-7] + ".log"
    os.makedirs(folder_path, mode=0o777, exist_ok=True)
    fp = open(log_path, 'x')
    fp.close()
    return log_path


def _delete_old_logs_when_logs_is_more_that(folder_path, how_many):
    list_of_files = os.listdir(folder_path)
    full_path = [(folder_path + "{0}").format(x) for x in list_of_files]

    if len(list_of_files) <= how_many:
        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)


def _log_without_exception(level, message):
    if level == "info":
        root.info(message)
    elif level == "warning":
        root.warning(message)
    elif level == "error":
        root.error(message)
    elif level == "debug":
        root.debug(message)
    elif level == "exception":
        root.exception(message)
    else:
        root.warning("Unrecognized log level, log message: " + message)


def _log_with_exception(level, message: str, exception: Exception):
    if level == "info":
        root.info(message + " - %s", exception, exc_info=True)
    elif level == "warning":
        root.warning(message + " - %s", exception, exc_info=True)
    elif level == "error":
        root.error(message + " - %s", exception, exc_info=True)
    elif level == "debug":
        root.debug(message + " - %s", exception, exc_info=True)
    elif level == "exception":
        root.exception(message + " - %s", exception, exc_info=True)
    else:
        root.warning("Unrecognized log level, log message: " + message + " + exception: " + str(exception))


def log_and_print(level, message, exception=None, force_print=False):
    if is_printing or force_print:
        print(message)

    level = level.lower()
    if exception is None:
        _log_without_exception(level, message)
    else:
        _log_with_exception(level, message, exception)


path = _prepare_folder_file_and_path(_log_folder)
_delete_old_logs_when_logs_is_more_that(_log_folder, 10)
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", path))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", _log_level_from_environment))
root.addHandler(handler)
