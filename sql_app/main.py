# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-27, Mon, 17:11
@Author: Jinpeng Yang
@Description: Main.py, combines all works
"""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    # 声明一个真实的session，并且用完时需要关闭
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get('/users/', response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user


@app.post('/users/{user_id}/items/', response_model=schemas.Item)
def create_item_for_user(
        user_id: int,
        item: schemas.ItemCreate,
        db: Session = Depends(get_db)
):
    return crud.create_user_item(db, item, user_id)


@app.get('/items/', response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip, limit)
    return items
