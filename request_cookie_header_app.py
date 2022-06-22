# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-21, Tue, 19:41
@Author: Jinpeng Yang
@Description: Header and Cookie Params
"""

from fastapi import FastAPI, Header, Cookie
from typing import Union


app = FastAPI()

@app.get("/items/")
async def get_item(
        *,
        cookie: Union[str, None] = Cookie(default=None),
        user_agent: str = Header(None),
        users_agent: str = Header(None)
):

    return {'cookie': cookie,
            'User_Agent': user_agent,
            'Users_Agent': users_agent
            }
