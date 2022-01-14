"""
Multi Application mounting
"""
from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from app.main import app as app1
from sql_app.main import app as app2
from sql_app2.main import app as app3

app = FastAPI(
    # servers=[
    #     {"url": "", "description": "Staging environment"},
    #     {"url": "", "description": "Production environment"},
    # ],
    # root_path="/api/v1",
    # root_path_in_servers=False,
)


@app.get("/test/")
def read_main(request: Request):
    return {"message": "Hello World from main app", "root_path": request.scope.get('root_path', '')}


# subapi = FastAPI()

# @subapi.get("/sub")
# def read_sub():
#     return {"message": "Hello World from sub API"}

# app.mount("/subapi", subapi)
app.mount("/app", app1)
app.mount("/sql_app", app2)
app.mount("/sql_app2", app3)
app.mount("/static", StaticFiles(directory="static"), name="static")
