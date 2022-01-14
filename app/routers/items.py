from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schema, crud
from app.dependencies import get_db

router = APIRouter(
    prefix="/items",
    tags=["Items"],
    # dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schema.Item])
async def read_item(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    Read items with all the information:
    \f
    :param limit:
    :param db:
    :param skip: User input.
    """
    return crud.get_items(db=db, skip=skip, limit=limit)
