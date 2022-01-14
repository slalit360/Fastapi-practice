"""
Dependencies
Sub-dependencies
Dependencies in path operation decorators
"""

from typing import Optional

from fastapi import FastAPI, Depends, Cookie, Header, HTTPException

app = FastAPI()


async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items_old/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users_old/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
# async def read_items(commons: Depends(CommonQueryParams)):
# async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
async def read_items(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items})
    return response


def query_extractor(q: Optional[str] = None):
    return q


def query_or_cookie_extractor(
        q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)
):
    print(last_query)
    if not q:
        return last_query
    return q


@app.get("/items_new/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor, use_cache=False)):
    return {"q_or_cookie": query_or_default}


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items_dep/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
