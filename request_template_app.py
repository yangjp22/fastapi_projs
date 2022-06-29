# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-29, Wed, 9:55
@Author: Jinpeng Yang
@Description: Jinja2 Templates Rendering Tutorials
"""

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
template = Jinja2Templates(directory='templates')


@app.get('/index', name='index')
async def index(request: Request):
    context = {'request': request, 'name': 'Index Fred'}
    return template.TemplateResponse('index.html', context=context)


@app.get('/app', name='app')
async def app(request: Request, username: str):
    context = {'request': request, 'name': 'App Fred', username: username}
    return template.TemplateResponse('app/app.html', context=context)
