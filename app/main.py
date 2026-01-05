from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import time
from typing import Callable
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.errors import DomainError
from lifespan import lifespan, limiter
from router import user_router, notification_router
import logging

logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)


@app.exception_handler(DomainError)
async def domain_exception_handler(
    request: Request, exc: DomainError
):
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.message}
    )


@app.exception_handler(Exception)
async def base_exception_handler(request: Request, exc: Exception):
    logger.exception(
        msg="An exception occured",
        extra={
            "url": str(request.url),
            "method": request.method,
        },
    )
    return JSONResponse(
        status_code=500, content={"detail": "Internal server error"}
    )


@app.middleware("http")
async def log_request(request: Request, call_next: Callable):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    duration_ms = duration * 1000
    logger.info(
        f"{request.method} {request.url.path} "
        f"-> {response.status_code} ({duration_ms:.1f}ms)"
    )
    return response


app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,  # ty:ignore[invalid-argument-type]
)
app.add_middleware(SlowAPIMiddleware)  # ty:ignore[invalid-argument-type]
app.include_router(user_router.router)
app.include_router(notification_router.router)


@app.get("/")
async def main():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=7000, reload=True)
