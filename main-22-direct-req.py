"""
Using the Request Directly
"""
from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/items/{item_id}")
def read_root(item_id: str, request: Request):
    client_host = request.client.host
    print(request.headers)

    print(request.method)
    print(dict(request.body()))
    return {"client_host": client_host, "item_id": item_id}
