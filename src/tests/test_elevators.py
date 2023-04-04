import json

import pytest

from app.api import crud


def test_all_elevators(test_app, monkeypatch):
    test_data = [
        {
            "id": 0,
            "floor": 2,
            "moving": False,
            "doors_opened": False,
            "last_movement": "2023-04-04T18:00:43",
        },
        {
            "id": 1,
            "floor": 4,
            "moving": False,
            "doors_opened": False,
            "last_movement": "2023-04-04T18:00:43",
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all_elevators", mock_get_all)

    response = test_app.get("/elevators/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_elevator_status(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "floor": 4,
        "moving": False,
        "doors_opened": False,
        "last_movement": "2023-04-04T18:00:43",
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get_elevator", mock_get)

    response = test_app.get("/elevators/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_elevator_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get_elevator", mock_get)

    response = test_app.get("/elevators/3")
    assert response.status_code == 404
    assert response.json()["detail"] == "Elevator not found"

    response = test_app.get("/elevators/0")
    assert response.status_code == 422
