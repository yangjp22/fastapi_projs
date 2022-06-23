# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-20, Mon, 17:45
@Author: Jinpeng Yang
@Description: Request Body
"""

from fastapi import FastAPI, Query, Path, Body
from fastapi.encoders import jsonable_encoder
from typing import Union
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()

@app.post('/items/')
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_after_tax = item.price + item.tax
        item_dict.update({'price_after_tax': price_after_tax})
    return item_dict

# @app.put('/items/{item_id}')
# async def create_item(item_id: int, item: Item):
#     return {'item_id': item_id, **item.dict()}

@app.put('/items/{item_id}')
async def create_item(
        *,
        item_id: int = Path(title='The ID of the item to get', le=1000, ge=0),
        q: Union[str, None] = None,
        item: Union[Item, None] = None,
):
    results = {'item_id': item_id}
    if q:
        results.update({'q': q})
    if item:
        results.update({'item': item})
    return results


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.put('/item-users/{item_id}')
async def create_item(
        item_id: int,
        item: Item,
        user: User,
        importance: int = Body(title="Importance")
):
    results = {'item_id': item_id, 'item': item, 'user': user, 'importance': importance}
    return results

@app.put('/item-embed/{item_id}')
async def create_item(
        item_id: int,
        item: Item = Body(embed=True)
):
    results = {'item_id': item_id, 'item': item}
    return results


class ItemUser(BaseModel):
    username: str
    description: Union[str, None] = Field(
        default=None,
        title="description of itemuser",
        max_length=300
    )
    price: float = Field(
        ge=0,
        description="the price must be greater than zero."
    )
    tax: Union[float, None] = None
    tags: list[str]


@app.post('/itemuser/')
async def create_item_user(
        item_user: ItemUser
):
    return item_user.dict()


class Image(BaseModel):
    url: str
    name: str


class ImgItem(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set()
    image: Union[Image, None] = None


@app.put('/images/{image_id}')
async def create_image(
        image_id: int,
        image_item: ImgItem
):
    results = {'img_id': image_id, 'img_item': image_item}
    return results


@app.put('/img/{image_id}')
async def update_img(
        image_id: int,
        weights: dict[int, float]
):
    [print(type(each)) for each in weights]
    return {
        'image_id': image_id,
        'weights': weights
    }


class UpdateItem(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/item-updates/{item_id}", response_model=UpdateItem, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


@app.put('/item-updates/{item_id}', response_model=UpdateItem)
async def update_item(item_id: str, item: UpdateItem):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    print(items[item_id])
    return update_item_encoded


@app.patch('/item-updates/{item_id}', response_model=UpdateItem)
async def update_item_partial(item_id: str,
                              item: UpdateItem):
    stored_data = items[item_id]
    stored_model = UpdateItem(**stored_data)
    update_model = item.dict(exclude_unset=True)
    updated_model = stored_model.copy(update=update_model)
    items[item_id] = jsonable_encoder(updated_model)
    return updated_model
