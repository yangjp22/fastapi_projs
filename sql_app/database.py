# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-27, Mon, 16:13
@Author: Jinpeng Yang
@Description: Database settings stuff
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# database urls
# 这也是链接不同数据库时需要更改的地方
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# connect_args={"check_same_thread": False} 只需要用在SQLite链接，其他数据库不需要此参数 需要可多线程
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal的实例便是真实的database session，即为一个能生产session的工厂
# autocommit 表示自动提交 autoflush表示自动刷新
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 继承Base的类能够创建database models or classes (the ORM models)
# 数据库表的结构用 ORM 的语言描述出来
Base = declarative_base()
