# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-19, Sun, 21:14
@Author: Jinpeng Yang
@Description: Path params and Query params
"""

from fastapi import FastAPI, Query, Path
from enum import Enum
from typing import Union


app = FastAPI()

@app.get('/')
async def index():
    return {"msg": "hello world"}

@app.get('/basic')
async def basic():
    return {'msg': 'This is a basic page'}

@app.get('/item/{item_id:int}')
async def get_item(item_id):
    print(type(item_id))
    return {'msg': item_id}


class ItemName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


@app.get('/item/{item_name}')
async def get_name(item_name: ItemName):
    if item_name == ItemName.alexnet:
        return {'item_name': item_name, 'msg': 'Deep learning FTW!'}
    if item_name.value == 'lenet':
        return {'item_name': item_name, 'msg': 'LeCNN all the images'}
    return {'item_name': item_name, 'msg': 'Have some residuals'}

@app.get('/files/{file_path:path}/index.html')
async def get_file(file_path):
    return {'file_path': file_path}

@app.get('/items/{item_id}')
async def get_item_cnt(item_id: int, q: str, skip: int = 0, limit: Union[str, None] = None):
    return {
        'item_id': item_id,
        'q': q,
        'skip': skip,
        'limit': limit
    }

@app.get('/items/')
async def read_items(q: Union[str, None] = None):
    results = {
        'items': [
            {'item_id': 'Foo'},
            {'item_id': 'Bar'}
        ]
    }
    if q:
        results.update({'q': q})
    return results

@app.get('/query_items/')
async def read_items(
        q: Union[str, None] = Query(
            default=...,
            max_length=50,
            # min_length=4,
            title="qTitle",
            deprecated=True,
            description='qDescr',
            alias='q-param'
        )
):
    results = {
        'items': [
            {'item_id': 'Foo'},
            {'item_id': 'Bar'}
        ]
    }
    if q:
        results.update({'q': q})
    return results

@app.get('/paths/{path_id}')
async def get_path(
        path_id: int = Path(title='The ID of the item to get', lt=10)
):
    return {'path_id': path_id + 10}
