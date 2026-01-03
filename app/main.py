import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.errors import DomainError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("app")

app = FastAPI()


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


@app.get("/")
def main():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=7000, reload=True)
