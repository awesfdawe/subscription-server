import logging
import sys
from functools import lru_cache
from os import getenv

import structlog
from litestar.logging.config import LoggingConfig, StructLoggingConfig
from structlog.stdlib import ProcessorFormatter
from structlog.types import Processor


def _get_shared_processors() -> list[Processor]:
    return [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]


def _get_processors(is_production: bool) -> list[Processor]:
    processors: list[Processor] = [
        structlog.stdlib.filter_by_level,
        *_get_shared_processors(),
    ]

    if is_production:
        processors.append(structlog.processors.dict_tracebacks)
        processors.append(structlog.processors.JSONRenderer(ensure_ascii=False))
    else:
        processors.append(structlog.processors.format_exc_info)
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    return processors


def _get_final_processor(is_production: bool) -> Processor:
    """Финальный рендерер для ProcessorFormatter.
    Применяется к чужим (uvicorn и т.д.) stdlib LogRecord-ам."""
    if is_production:
        return structlog.processors.JSONRenderer(ensure_ascii=False)
    return structlog.dev.ConsoleRenderer(colors=True)


@lru_cache(maxsize=1)
def get_logging_config() -> StructLoggingConfig:
    env = getenv("ENVIRONMENT", "DEV")
    if env not in ("DEV", "PRODUCTION"):
        print(  # noqa: T201
            f"Critical error: invalid ENVIRONMENT variable: '{env}'. Must be 'DEV' or 'PRODUCTION'",
            file=sys.stderr,
        )
        sys.exit(1)

    is_production = env == "PRODUCTION"

    log_level = getenv("LOG_LEVEL", "INFO")
    if not hasattr(logging, log_level):
        print(  # noqa: T201
            f"Critical error: invalid LOG_LEVEL variable: '{log_level}'",
            file=sys.stderr,
        )
        sys.exit(1)

    return StructLoggingConfig(
        processors=_get_processors(is_production=is_production),
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
        standard_lib_logging_config=LoggingConfig(
            log_exceptions="always",
            formatters={
                "structlog_plain": {
                    "format": "%(message)s",
                },
                "structlog_foreign": {
                    "()": ProcessorFormatter,
                    "processor": _get_final_processor(is_production),
                    "foreign_pre_chain": _get_shared_processors(),
                },
            },
            handlers={
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "structlog_plain",
                },
                "queue_listener": {
                    "class": "logging.handlers.QueueHandler",
                    "handlers": ["console"],
                    "queue": {"()": "queue.Queue", "maxsize": -1},
                    "listener": "litestar.logging.standard.LoggingQueueListener",
                },
                "foreign_console": {
                    "class": "logging.StreamHandler",
                    "formatter": "structlog_foreign",
                },
            },
            loggers={
                "uvicorn": {
                    "handlers": ["foreign_console"],
                    "level": log_level,
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["foreign_console"],
                    "level": log_level,
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["foreign_console"],
                    "level": log_level,
                    "propagate": False,
                },
            },
            root={"handlers": ["queue_listener"], "level": log_level},
        ),
    )


def setup_logging() -> None:
    config = get_logging_config()
    config.configure()
    if config.standard_lib_logging_config:
        config.standard_lib_logging_config.configure()


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
