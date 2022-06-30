# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-30, Thu, 0:38
@Author: Jinpeng Yang
@Description: 数据表的增删查改操作
"""

from sqlalchemy.orm import Session

from proj_covid import models, schemas


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, province: str):
    return db.query(models.City).filter(models.City.province == province).first()


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.City).order_by(models.City.country_code).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CreateCity):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_data(db: Session, city: str = None, skip: int = 0, limit: int = 10):
    if city:
        return db.query(models.Data).filter(models.Data.city.has(province=city))
    return db.query(models.Data).order_by(models.Data.confirmed.desc()).offset(skip).limit(limit).all()


def create_city_data(db: Session, city_id: int, data: schemas.CreateData):
    db_data = models.Data(**data.dict(), city_id=city_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
