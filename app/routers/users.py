from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session


from ..dependencies import get_db 
from ..db import crud, models, schemas, database


models.Base.metadata.create_all(bind=database.engine)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}}
    )



@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db), guest: bool=True):
    db_user = crud.get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db, user, guest)

@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: id, user: schemas.User, db: Session=Depends(get_db)):
    user_db = crud.get_user(db, user_id)
    if not user_db:
        return HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, user_id, dict(user))

@router.get("/leaderboard", response_model=List[schemas.UserLeaderboard])
def leaderboard(db: Session = Depends(get_db)):
    users = crud.leaderboard(db)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session=Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/position/{user_id}", response_model=schemas.UserPosition)
def read_user(user_id: int, db: Session=Depends(get_db)):
    rank = crud.get_rank(db, user_id)
    db_user = crud.get_user(db, user_id)
    user = schemas.UserPosition(**db_user, rank=rank)
    return user
    
