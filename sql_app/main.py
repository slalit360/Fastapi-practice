from functools import lru_cache
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import schema, crud, models, config
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


@lru_cache()
def get_settings():
    return config.Settings()


app = FastAPI(openapi_url="")


# @app.middleware("http")
# async def db_session_middleware(request: Request, call_next):
#     response = Response("Internal server error", status_code=500)
#     try:
#         request.state.db = SessionLocal()
#         response = await call_next(request)
#     finally:
#         request.state.db.close()
#     return response
#
#
# Dependency for python 3.6 and below
# def get_db(request: Request):
#     return request.state.db

def get_db():  # for python 3.7+
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/info")
async def info(settings: config.Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }


@app.post("/users/", response_model=schema.User)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db=db, email=user.email):
        raise HTTPException(status_code=400, detail="User with email id already exist!")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schema.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)


@app.get("/users/{user_id}/", response_model=schema.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User not found with this user id : {user_id}")
    return db_user


@app.get("/user/{email}/", response_model=schema.User)
async def read_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User not found with this email id : {email}")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schema.Item)
async def create_item_for_user(user_id: int, item: schema.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, user_id=user_id, item=item)


@app.get("/items/", response_model=List[schema.Item])
async def read_item(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db=db, skip=skip, limit=limit)
