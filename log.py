import logging.handlers
import os
from datetime import datetime

from main import main

handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "\log\\" + str(datetime.now()) + ".log"))
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
