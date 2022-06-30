# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-30, Thu, 0:8
@Author: Jinpeng Yang
@Description: 数据库的相关项和连接
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./coronavirus.sqlite3'
# SQLALCHEMY_DATABASE_URL = 'postgresql://username:password@host:port/database_name'

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       encoding='utf-8',
                       echo=True,
                       connect_args={'check_same_thread': False})

# 在SQLAlchemy中，CRUD都是通过会话(session)进行的，所以我们必须先创建会话
# 每一个SessionLocal实例就是一个session
# flush()是指发送数据库语句到数据库，但数据库不一定执行写入磁盘; commit()是指提交事务，将变更保存到数据库文件
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)

# 创建基本映射类
Base = declarative_base(bind=engine, name='Base')
