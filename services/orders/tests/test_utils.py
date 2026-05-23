import logging

logger = logging.getLogger("tests.utils")


def log_assert_equal(expected, actual, description: str):
    """Log expected vs actual and assert equality."""
    logger.info("[ASSERT] %s | Expected: %r | Received: %r", description, expected, actual)
    assert expected == actual


def log_info(message: str):
    logger.info(message)
