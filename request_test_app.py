# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-28, Tue, 17:9
@Author: Jinpeng Yang
@Description: Application for testing
"""

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Union

fake_secret_token = "coneofsilence"

fake_db = {
    'foo': {'id': 'foo', 'title': 'Foo', 'description': 'There goes my hero'},
    'bar': {'id': 'bar', 'title': 'Bar', 'description': 'The bartenders'}
}

app = FastAPI()


@app.get('/')
async def read_main():
    return {'msg': 'Hello World'}


class Item(BaseModel):
    id: str
    title: str
    description: Union[str, None] = None


@app.get('/items/{item_id}', response_model=Item)
async def read_item(item_id: str,  x_token: str = Header()):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail='Invalid X-Token header')
    if item_id not in fake_db:
        raise HTTPException(status_code=400, detail='Item not found')
    return fake_db[item_id]


@app.post('/items/', response_model=Item)
async def create_item(item: Item, x_token: str = Header()):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail='Invalid X-Token header')
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail='Item already exists')
    fake_db[item.id] = item.dict()
    return item
