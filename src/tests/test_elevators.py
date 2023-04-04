import json

import pytest

from app.api import crud


def test_all_elevators(test_app, monkeypatch):
    test_data = [
        {"id": 1, "floor": 2},
        {"id": 1, "floor": 4},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/elevators/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_elevator_status(test_app, monkeypatch):
    test_data = {"id": 1, "floor": 2}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/elevators/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_elevator_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/elevators/150")
    assert response.status_code == 404
    assert response.json()["detail"] == "Elevator not found"


def test_create_elevator(test_app, monkeypatch):
    test_request_payload = {"floor": 1}
    test_response_payload = {"id": 1, "floor": 1}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(
        "/elevators/",
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_elevator_invalid_json(test_app):
    response = test_app.post("/elevators/", content=None)
    assert response.status_code == 422
