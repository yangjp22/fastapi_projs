# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-27, Mon, 14:7
@Author: Jinpeng Yang
@Description: Middleware Tutorial
"""

import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# 定义一个中间件：对进入的request 和 返回的response进行处理
@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


origins = [
    'http://localhost.tiangolo.com',
    'https://localhost.tiangolo.com',
    'http://localhost',
    'http://localhost:8080',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=['*']
)


@app.get("/")
async def main():
    return {'msg': 'hello world'}