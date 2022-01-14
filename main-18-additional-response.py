"""
Additional Responses in OpenAPI
"""
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from starlette.responses import Response


class Item(BaseModel):
    id: str
    value: str


app = FastAPI()


responses = {
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}


@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        **responses,
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }
    },
)
async def read_item(item_id: str, img: Optional[bool] = None):
    if img:
        return FileResponse("static/new_pic.jpg", media_type="image/jpg")
    else:
        return {"id": "foo", "value": "there goes my hero"}
