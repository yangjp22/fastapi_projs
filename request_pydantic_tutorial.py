# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-29, Wed, 16:48
@Author: Jinpeng Yang
@Description: Pydantic Tutorial
"""

from datetime import datetime
from pydantic import BaseModel
from typing import Union, List, Optional

"""
Data validation and settings management using python type annotations.
使用Python的类型注解来进行数据校验和settings管理

pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.
Pydantic可以在代码运行时提供类型提示，数据校验失败时提供友好的错误提示

Define how data should be in pure, canonical python; validate it with pydantic.
定义数据应该如何在纯规范的Python代码中保存，并用Pydantic验证它
"""

class User(BaseModel):
    id: int
    name: str = 'John Snow'
    signup_ts: Optional[datetime] = None
    friends: list[str] = []


external_data = {
    'id': '123',
    'signup_ts': '2022-12-22 12:22',
    'friends': [1, 2, '3']  # 3是可以int('3')的
}

user = User(**external_data)
print(repr(user.signup_ts))


# Pydantic实例的方法
print(user.dict())
print(user.copy())   # 浅拷贝
print(user.json())
print(user.schema())
print(user.schema_json())
print(User.construct(external_data))   # 不校验数据，不推荐使用
print(User.parse_obj(external_data))
print(User.__fields__.keys())
# print(User.parse_raw('{...}'))
# print(User.parse_file('filepath'))




