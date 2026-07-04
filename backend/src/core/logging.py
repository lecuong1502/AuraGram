import logging
import sys
from src.core.config import settings


def setup_logging() -> None:
    """Configure structured logging for the application."""
    level = logging.DEBUG if settings.DEBUG else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Suppress noisy third-party loggers in production
    if not settings.DEBUG:
        logging.getLogger("motor").setLevel(logging.WARNING)
        logging.getLogger("beanie").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


# Module-level logger for convenience
logger = logging.getLogger("auragram")
