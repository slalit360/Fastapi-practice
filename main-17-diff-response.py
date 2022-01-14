"""
Custom Response - HTML, Stream, File, others
"""

from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, ORJSONResponse, UJSONResponse
from pydantic import BaseModel
from starlette.responses import HTMLResponse, PlainTextResponse, RedirectResponse, StreamingResponse, FileResponse


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    # return JSONResponse(content=json_compatible_item_data)
    return item


@app.get("/legacy/")
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")


@app.get("/item/", response_class=ORJSONResponse)
async def read_items():
    return [{"item_id": "Foo"}]


@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    html_content = """
        <html>
            <head>
                <title>Some HTML in here</title>
            </head>
            <body>
                <h1>Look ma! HTML!</h1>
            </body>
        </html>
        """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/", response_class=PlainTextResponse)
async def main():
    return "Hello World"


@app.get("/newjson/", response_class=UJSONResponse)
async def read_items():
    return [{"item_id": "Foo"}]


@app.get("/typer",response_class=RedirectResponse)
async def redirect_typer():
    return RedirectResponse("https://typer.tiangolo.com")


@app.get("/pydantic", response_class=RedirectResponse, status_code=302)
async def redirect_pydantic():
    return "https://pydantic-docs.helpmanual.io/"


async def fake_video_streamer():
    for i in range(1000):
        yield b"some fake video bytes\t"


@app.get("/media_stream/", response_class=StreamingResponse)
async def media_stream():
    return StreamingResponse(fake_video_streamer())


@app.get("/play_video/")
def play_video():
    def iterfile():  #
        with open("static/new.mp4", mode="rb") as file_like:  #
            yield from file_like  #
    return StreamingResponse(iterfile(), media_type="video/mp4")


@app.get("/download_file", response_class=FileResponse)
async def download_file():
    # return "log.txt"
    return FileResponse("static/log.txt", media_type='application/octet-stream', filename="log.txt")