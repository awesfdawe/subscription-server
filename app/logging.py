import inspect
import logging
import sys
from os import getenv

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame = inspect.currentframe()
        depth = 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    log_level = logging.getLevelNamesMapping().get(getenv("LOG_LEVEL"), logging.INFO)

    logger.remove()
    logger.add(sys.stderr, level=log_level, enqueue=True)

    intercept_handler = InterceptHandler()

    logging.basicConfig(handlers=[intercept_handler], level=log_level, force=True)

    for module in ("uvicorn", "apscheduler", "watchfiles"):
        mod_logger = logging.getLogger(module)
        mod_logger.handlers.clear()
        mod_logger.handlers = [intercept_handler]
        mod_logger.propagate = False
