from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import schema, crud
from app.dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=schema.User)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db=db, email=user.email):
        raise HTTPException(status_code=400, detail="User with email id already exist!")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[schema.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)


@router.get("/{user_id}/", response_model=schema.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User not found with this user id : {user_id}")
    return db_user


@router.get("/{email}", response_model=schema.User)
async def read_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User not found with this email id : {email}")
    return db_user


@router.post("/{user_id}/items/", response_model=schema.Item)
async def create_item_for_user(user_id: int, item: schema.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, user_id=user_id, item=item)
