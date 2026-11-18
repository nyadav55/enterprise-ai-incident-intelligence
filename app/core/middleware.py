

import logging
import time

from fastapi import Request

# Get the centralized application logger.
logger = logging.getLogger("eaiirp")


async def request_logging_middleware(request: Request, call_next):
    # Record when the request starts.
    start_time = time.perf_counter()

    logger.info(
        "Request started: %s %s",
        request.method,
        request.url.path,
    )

    try:
        # Pass the request to the next middleware or API endpoint.
        response = await call_next(request)

        # Calculate request processing time in milliseconds.
        duration_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            "Request completed: %s %s | Status: %s | Duration: %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response

    except Exception:
        # Capture unexpected errors with their traceback.
        logger.exception(
            "Request failed: %s %s",
            request.method,
            request.url.path,
        )
        raise
