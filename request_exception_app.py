# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-22, Wed, 15:40
@Author: Jinpeng Yang
@Description: Handling Errors
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

items = {'foo': 'The foo wrestlers'}

@app.get('/item/{item_id}')
async def get_item(item_id: str):
    if item_id not in items:
        # raise HTTPException(status_code=404, detail='Item not found')
        err_message = {'msg': "Item not found", 'date': '2022-06-22'}
        raise HTTPException(status_code=404, detail=err_message, headers={'X-Error': "There goes my error."})
    return {'items': items[item_id]}


class MyOwnException(Exception):
    def __init__(self, name):
        self.name = name


@app.exception_handler(MyOwnException)
async def myown_exception_handler(request: Request, exc: MyOwnException):
    return JSONResponse(
        status_code=418,
        content={
            'msg': "Oops, {} did something wrong".format(exc.name)
        }
    )

@app.get('/items/{name}')
async def read_item(name: str):
    if name == 'yolo':
        raise MyOwnException(name=name)
    return {'name': name}
