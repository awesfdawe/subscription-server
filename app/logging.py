import inspect
import logging
import sys

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
    logger.remove()
    logger.add(sys.stderr, level=20, enqueue=True)

    intercept_handler = InterceptHandler()

    logging.basicConfig(handlers=[intercept_handler], level=20, force=True)

    for module in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        mod_logger = logging.getLogger(module)
        mod_logger.handlers.clear()
        mod_logger.handlers = [intercept_handler]
        mod_logger.propagate = False
