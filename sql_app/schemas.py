# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-27, Mon, 16:38
@Author: Jinpeng Yang
@Description: Schemas, knows as Pydantic models as well
"""

from typing import Union
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(BaseModel):
    id: int
    is_active: bool = True
    items: list[Item] = []

    class Config:
        # 和数据库模型能够相互结合 可以给数据库出来的数据进行验证和筛选
        orm_mode = True
