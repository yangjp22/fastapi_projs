# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-28, Tue, 0:8
@Author: Jinpeng Yang
@Description: Dependencies file for each routers
"""

from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header()):
    if x_token != 'fake-super-secret-token':
        raise HTTPException(status_code=400, detail='X-Token header invalid')


async def get_query_token(token: str):
    if token != 'jessica':
        raise HTTPException(status_code=400, detail="No Jessica token provided")
