# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-22, Wed, 0:13
@Author: Jinpeng Yang
@Description: Form Data
"""

from fastapi import FastAPI, Form, File, UploadFile, Body
from pydantic import BaseModel


app = FastAPI()


@app.post('/user/')
async def create_user(
        *,
        username: str = Form(...),
        pwd: str = Form(...)
):
    return {'user': username, 'password': pwd}


@app.post('/file/')
async def create_file(
        *,
        file: bytes = File()
):
    print(type(file))
    print(dir(file))
    return {'file': file}


@app.post('/uploadfile/')
async def create_file(
        *,
        file: UploadFile
):
    print(type(file))
    print(dir(file.file))
    return {'file': file}


@app.post('/uploadfiles/')
async def create_files(
        *,
        file: list[UploadFile]
):
    print(type(file))
    print(type(file[0]))
    print(dir(file[0].file))
    return {'file': file}


@app.post('/uploadfilesform/')
async def create_files(
        *,
        username: str = Form(),
        pwd: str = Form(),
        file: UploadFile
):
    print(type(file))
    print(dir(file.file))
    return {'file': file, 'name': username, 'pwd': pwd}


@app.post('/uploadfilesformwithbody/')
async def create_files(
        *,
        body: str = Body(),
        username: str = Form(),
        pwd: str = Form(),
        file: UploadFile
):
    print(type(file))
    print(type(body))
    print(type(username))
    return {'file': file, 'name': username, 'pwd': pwd, 'body': body}


class Item(BaseModel):
    name: str
    price: float


@app.post('/uploadfilesformwithbodymodel/')
async def create_files(
        *,
        item: Item,
        body: str = Body(),
        username: str = Form(),
        pwd: str = Form(),
        file: UploadFile
):
    print(type(file))
    print(type(item))
    print(type(body))
    print(type(username))
    return {'file': file, 'name': username, 'pwd': pwd, 'body': body, 'item': item}
