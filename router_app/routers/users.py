# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-28, Tue, 0:2
@Author: Jinpeng Yang
@Description: APIRouter for users
"""

from fastapi import APIRouter

router = APIRouter()


@router.get('/users/', tags=['users'])
async def read_users():
    return [{'username': 'Rick'}, {'username': 'Morty'}]


@router.get('/users/me', tags=['users'])
async def read_user_me():
    return {'username': 'fakecurrentuser'}


@router.get('/users/{username}', tags=['users'])
async def read_user(username: str):
    return {'username': username}
