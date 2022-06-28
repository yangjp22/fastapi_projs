# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-28, Tue, 11:55
@Author: Jinpeng Yang
@Description: router for admin
"""

from fastapi import APIRouter

router = APIRouter()


@router.post('/')
async def update_admin():
    return {'msg': 'Admin getting schwifty'}

