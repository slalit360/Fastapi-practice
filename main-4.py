"""
Body - Multiple Parameters & Fields & Nested Fields
"""
from typing import Optional, List, Set

from fastapi import Body, FastAPI, Query, Path
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None
    tags: Set[str] = set()
    images: Optional[List[Image]] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]


@app.put("/items/{item_id}")
async def update_item(*, item_id: int,
                      item: Item = Body(...),
                      user: User,
                      importance: int = Body(...)):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images