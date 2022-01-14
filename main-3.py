"""
Path Parameters and Numeric Validations. : Path(...)
"""

from typing import Optional

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items_new/{item_id}")
async def read_items(
    *,
        item_id: int = Path(..., title="The ID of the item to get", gt=0, le=1000),
        q: float = Query(..., gt=0, lt=10.5)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results