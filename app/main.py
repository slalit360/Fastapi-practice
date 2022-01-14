import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from starlette.testclient import TestClient

from app.models import Item
from .database import engine
from .routers import users, items
from . import models

models.Base.metadata.create_all(bind=engine)

description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(
    title="ChimichangApp",
    description=description,
    version="1.0.1",
    terms_of_service="http://example.com/terms/",
    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url="/docs",
    redoc_url=None,
)

app.include_router(users.router)

app.include_router(items.router)

app.mount("/static/", StaticFiles(directory="static"), name="static")


@app.get("/", tags=['Application'], openapi_extra={"x-aperture-labs-portal": "blue"})
async def root():
    return {"msg": "Hello World"}


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


client = TestClient(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)