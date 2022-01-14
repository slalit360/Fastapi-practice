"""
Cookie Parameters and Header Parameters
"""
from typing import Optional, List

from fastapi import Cookie, FastAPI, Header

app = FastAPI()


@app.get("/items_cookie/")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}


@app.get("/items_header/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}


@app.get("/items_custom_header/")
async def read_items(
    strange_header: Optional[str] = Header(None, convert_underscores=False)
):
    return {"strange_header": strange_header}


@app.get("/items_header_multivalue/")
async def read_items(x_token: Optional[List[str]] = Header(None)):
    return {"X-Token values": x_token}

