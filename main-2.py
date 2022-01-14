"""
Query parameters and String validation : Query(...) | Query(None) | Query("default")
request Body : Body(...) | Body(None)
"""

from typing import Optional, List

from fastapi import FastAPI, Body, Query
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI(version="2.4.6")


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    # return {"item_id": item_id, **item.dict()}
    return {"item_id": item_id, "data": item}


@app.put("/items_new/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


@app.put("/items_new2/{item_id}")
async def update_item(item_id: int, item: Item, importance: dict = Body(...)):
    results = {"item_id": item_id, "item": item, "importance": importance}
    return results


# @app.get("/items/")
# async def read_items(q: str = Query(..., min_length=3, max_length=50, regex="^[a-zA-Z]{4,}$")):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^[a-zA-Z]{4,}$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items_list/")
async def read_items(p: List[str] = Query(..., title="Query P", alias="item-p"),
                     q: List[str] = Query([], title="Query Q", description="Query string for the items to search")):
    query_items = {"p": p, "q": q}
    return query_items


@app.get("/items_list2/")
async def read_items(
        q: Optional[str] = Query(
            None,
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            regex="^[a-zA-Z]{4,}$",
            deprecated=True,
        )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
