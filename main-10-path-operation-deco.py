"""
Path Operation Configuration: status , tags, information like summary, description, response_description, deprecated

jsonable_encoder
"""
from datetime import datetime
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel
from starlette import status
from fastapi.encoders import jsonable_encoder

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()


@app.post("/items/",
          response_model=Item,
          tags=["items"],
          status_code=status.HTTP_201_CREATED,
          summary="Create an new item",
          description="Create an item with all the information, name, description, price, tax and a set of unique tags",
          response_description="The created item",
          )
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"], deprecated=True)
async def read_items():
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]


class Item2(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None


fake_db = {}


@app.put("/items/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_item(id: str, item: Item2):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    print(fake_db)
    