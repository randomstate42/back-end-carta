from sqlalchemy.orm import Session
from sqlalchemy import desc, func

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id==user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username==username).first()

def leaderboard(db: Session):
    return db.query(models.User).order_by(desc(models.User.score)).offset(0).limit(100)
    
def get_rank(db: Session, user_id: id):
    return db.query(
        models.User,
        func.rank().filter(models.User.id==user_id)\
        .over(order_by=models.User.score)
        )

def create_user(db: Session, user: schemas.UserCreate, guest: bool=True):
    username = "Guest"+str(user.id) if guest else user.username
    db_user = models.User(username=username, picture=user.picture)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: id, update_data: dict):
    return db.query(models.User)\
        .filter(models.User.id==user_id)\
        .update(update_data, synchronize_session=True)
