from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def root():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Hello User, welcome to todolist server"},
    )
