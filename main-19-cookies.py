"""
Response Cookies
"""
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response


class Item(BaseModel):
    id: str
    value: str


app = FastAPI()


@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}

