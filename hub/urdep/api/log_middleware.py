import logging

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger('urdep')

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        logger.info(
            "API request",
            extra={
                "request": { "method": request.method, "url": str(request.url) },
                "response": { "status_code": response.status_code, },
            },
        )
        return response
