from datetime import datetime

from fastapi import Request, Response

from utils.logging_config import LoggingConfig

logger = LoggingConfig.get_logger(__name__)


async def log_requests_middleware(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")

    start_time = datetime.now()
    response: Response = await call_next(request)
    process_time = datetime.now() - start_time

    logger.info(
        f"Request completed: {request.method} {request.url} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time.total_seconds():.2f}s"
    )

    return response
