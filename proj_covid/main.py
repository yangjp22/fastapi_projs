# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-29, Wed, 17:24
@Author: Jinpeng Yang
@Description: Main File for Covid19 Project, 主接口文件和应用程序
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api import coronavirus_router


app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(coronavirus_router.router,
                   prefix='/coronavirus',
                   tags=['Coronavirus'])


@app.get('/')
async def index():
    return {'msg': 'hello world'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True, debug=True, workers=4)
