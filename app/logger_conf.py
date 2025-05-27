import logging
import sys

logger = logging.getLogger("custom_logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(levelname)s: ->  [%(filename)s:%(lineno)d] msg:" %(message)s " %(asctime)s',
    datefmt="%H:%M:%S",
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Optional: save logs in a file

# file_handler = logging.FileHandler("app.log", encoding="utf-8")
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

logger.propagate = False
