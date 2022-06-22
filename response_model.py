# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-21, Tue, 21:46
@Author: Jinpeng Yang
@Description: Response Model
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list[str] = []


class ItemOut(BaseModel):
    name: str
    price: float
    price_after_tax: Union[float, None] = None


@app.post('/items/', response_model=ItemOut)
async def create_item(item: Item):
    return item


class UserIn(BaseModel):
    name: str
    pwd: str
    age: int


class UserOut(BaseModel):
    name: str
    age: int


class UserInDB(BaseModel):
    name: str
    hashed_pwd: str
    age: int


def fake_hashed_pwd(pwd: str):
    return "hashed_" + pwd


def fake_save_user_to_db(user_in: UserIn):
    hashed_pwd = fake_hashed_pwd(user_in.pwd)
    user_in_db = UserInDB(**user_in.dict(), hashed_pwd=hashed_pwd)
    return user_in_db


@app.post('/user/', response_model=UserOut)
async def create_user(user: UserIn):
    user_in_db = fake_save_user_to_db(user)
    return user_in_db
