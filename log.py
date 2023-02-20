import logging.handlers
import os
from datetime import datetime

from main import main


def _prepare_folder_file_and_path(folder_path):
    log_path = folder_path + str(datetime.now()).replace(" ", "_", 10).replace(":", "-")[:-7] + ".log"
    os.makedirs(folder_path, mode=0o777, exist_ok=True)
    fp = open(log_path, 'x')
    fp.close()
    return log_path


def _delete_old_logs_when_logs_is_more_that(folder_path, how_many):
    list_of_files = os.listdir(folder_path)

    if len(list_of_files) >= how_many:
        oldest_file = min(list_of_files, key=os.path.getctime)
        os.remove(os.path.abspath(oldest_file))


log_folder = "log\\"
path = _prepare_folder_file_and_path(log_folder)
_delete_old_logs_when_logs_is_more_that(log_folder, 1000)
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", path))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
root.addHandler(handler)

try:
    exit(main())
except Exception:
    logging.exception("Exception in main()")
    exit(1)
