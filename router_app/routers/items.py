# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-28, Tue, 0:12
@Author: Jinpeng Yang
@Description: Routers for items
"""

from fastapi import APIRouter, HTTPException, Depends

from ..dependencies import get_token_header


router = APIRouter(
    prefix='/items',
    tags=['items'],
    dependencies=[Depends(get_token_header)],
    responses={404: {'description': 'Not found'}}
)


fake_items_db = {'plumbus': {'name': 'Plumbus'}, 'gun': {'name': "Portal Gun"}}


@router.get('/')
async def read_items():
    return fake_items_db


@router.get('/{item_id}', tags=['items'])
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=400, detail="Item not found")
    return {'name': fake_items_db[item_id]['name'], 'item_id': item_id}


@router.put(
    '/{item_id}',
    tags=['custom'],
    responss={403: {'description': 'Operation forbidden'}}
)
async def update_item(item_id: str):
    if item_id != 'plumbus':
        raise HTTPException(status_code=403, detail='You can only update the item: plumbus')
    return {'item_id': item_id, 'name': 'The great Plumbus'}
