# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-28, Tue, 11:53
@Author: Jinpeng Yang
@Description: Main module, ties everything together
"""

from fastapi import FastAPI, Depends

from .dependencies import get_token_header, get_query_token
from .routers import items, users
from .internal import admin


app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(get_token_header)],
    responses={418: {'description': 'I am a teapot'}}
)


@app.get('/')
async def root():
    return {'msg': "Hello Bigger Application"}
