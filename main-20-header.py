"""
Response Headers
"""
from fastapi import FastAPI, Response
from starlette.responses import JSONResponse

app = FastAPI()


@app.get("/headers-and-object/")
def get_headers(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Hello World"}


@app.get("/headers/")
def get_headers():
    content = {"message": "Hello World"}
    headers = {"X-Name": "alone in the world", "Content-Language": "en-US"}
    return JSONResponse(content=content, headers=headers)