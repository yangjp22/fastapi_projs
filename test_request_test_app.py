# -*- coding:utf-8 -*-
"""
@Created on: 2022-06-28, Tue, 17:12
@Author: Jinpeng Yang
@Description: Test the main.py file
"""

from fastapi.testclient import TestClient

from request_test_app import app

client = TestClient(app)


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


# correct token
def test_read_item():
    response = client.get('/items/foo', headers={'X-Token': 'coneofsilence'})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero"
    }


def test_read_item_bad_token():
    response = client.get('/items/foo', headers={'X-Token': 'hailhydra'})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent_item():
    response = client.get('/items/zac', headers={'X-Token': 'coneofsilence'})
    assert response.status_code == 400
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        '/items/',
        headers={'X-Token': 'coneofsilence'},
        json={"id": "zac", "title": "Zac", "description": "Best jungler"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "zac",
        "title": "Zac",
        "description": "Best jungler"
    }


def test_create_item_bad_token():
    response = client.post(
        '/items/',
        headers={'X-Token': 'hailhydra'},
        json={"id": "zac", "title": "Zac", "description": "Best jungler"}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid X-Token header"
    }


def test_create_existing_item():
    response = client.post(
        '/items/',
        headers={'X-Token': 'coneofsilence'},
        json={"id": "foo", "title": "Foo", "description": "There goes my hero"}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Item already exists"
    }
