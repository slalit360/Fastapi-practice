"""
Advanced Middleware
"""
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
# from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "*"])
app.add_middleware(GZipMiddleware, minimum_size=10)
# app.add_middleware(HTTPSRedirectMiddleware)


@app.get("/")
async def main():
    return {"message": "Hello World"}
