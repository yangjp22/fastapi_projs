# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-19, Sun, 21:11
@Author: Jinpeng Yang
@Description: 
"""
from fastapi import FastAPI


app = FastAPI()

@app.get('/')
async def index():
    return {"msg": "hello world"}