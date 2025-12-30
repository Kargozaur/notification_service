import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def main():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=7000, reload=True)
