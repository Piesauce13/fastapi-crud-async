import json

import pytest

from app.api import events_crud


def test_create_event(test_app, monkeypatch):
    payload = {
        "title": "Concert",
        "city": "Paris",
        "price_usd": 25,
        "seats_left": 100,
    }

    async def mock_post(event):
        return 1

    monkeypatch.setattr(events_crud, "post", mock_post)
    response = test_app.post("/events/", content=json.dumps(payload))

    assert response.status_code == 201
    assert response.json() == {"id": 1, **payload}


def test_read_event(test_app, monkeypatch):
    event = {
        "id": 1,
        "title": "Concert",
        "city": "Paris",
        "price_usd": 25,
        "seats_left": 100,
    }

    async def mock_get(id):
        return event

    monkeypatch.setattr(events_crud, "get", mock_get)
    response = test_app.get("/events/1/")

    assert response.status_code == 200
    assert response.json() == event


def test_read_missing_event(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(events_crud, "get", mock_get)
    response = test_app.get("/events/999/")

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


@pytest.mark.parametrize(
    "event_id, payload",
    [
        (0, {"title": "Concert", "city": "Paris", "price_usd": 25, "seats_left": 100}),
        (1, {"title": "Hi", "city": "Paris", "price_usd": 25, "seats_left": 100}),
    ],
)
def test_update_event_invalid(test_app, monkeypatch, event_id, payload):
    async def mock_get(id):
        return None

    monkeypatch.setattr(events_crud, "get", mock_get)
    response = test_app.put(
        f"/events/{event_id}/", content=json.dumps(payload)
    )

    assert response.status_code == 422


def test_delete_event(test_app, monkeypatch):
    event = {
        "id": 1,
        "title": "Concert",
        "city": "Paris",
        "price_usd": 25,
        "seats_left": 100,
    }

    async def mock_get(id):
        return event

    async def mock_delete(id):
        return id

    monkeypatch.setattr(events_crud, "get", mock_get)
    monkeypatch.setattr(events_crud, "delete", mock_delete)
    response = test_app.delete("/events/1/")

    assert response.status_code == 200
    assert response.json() == event
