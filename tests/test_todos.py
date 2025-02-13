import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_get_empty_todos(test_app, async_client):
    response = await async_client.get("/api/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == []


@pytest.mark.asyncio
async def test_post_todos(test_app, async_client):
    todo_data = {
        "name": "Купить продукты",
        "description": "Молоко, хлеб, яйца",
        "completed": False,
    }
    response = await async_client.post("/api/todos/", json=todo_data)
    print(response.json())
    assert response.status_code == 201
    assert response.json() == {"id": 1, **todo_data}


@pytest.mark.asyncio
async def test_update_todos(test_app, async_client):
    todo_data = {
        "name": "Купить продукты",
        "description": "Молоко, хлеб, яйца",
        "completed": False,
    }
    response = await async_client.post("/api/todos/", json=todo_data)
    assert response.status_code == 201

    todo_id = response.json()["id"]

    updated_todo_data = {"completed": True}
    update_response = await async_client.patch(
        f"/api/todos/{todo_id}", json=updated_todo_data
    )
    assert update_response.status_code == 200

    assert update_response.json() == {
        "id": todo_id,
        "name": "Купить продукты",
        "description": "Молоко, хлеб, яйца",
        "completed": True,
    }


@pytest.mark.asyncio
async def test_delete_todos(test_app, async_client):
    todo_data = {
        "name": "Купить продукты",
        "description": "Молоко, хлеб, яйца",
        "completed": False,
    }
    response = await async_client.post("/api/todos/", json=todo_data)
    assert response.status_code == 201

    todo_id = response.json()["id"]

    delete_response = await async_client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 204

    second_delete_response = await async_client.delete(f"/api/todos/{todo_id}")
    assert second_delete_response.status_code == 404
