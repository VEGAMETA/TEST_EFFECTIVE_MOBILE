import pytest
from httpx import AsyncClient

base_url = "http://127.0.0.1:8000"


@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.post("/products", json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 100.0,
            "quantity": 10
        })
    assert response.status_code == 200
    assert response.json().get("name") == "Test Product"
    assert response.json().get("quantity") == 10


@pytest.mark.asyncio
async def test_get_products():
    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.get("/products")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_get_product_by_id():
    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.post("/products", json={
            "name": "Another Product",
            "description": "Another Description",
            "price": 150.0,
            "quantity": 5
        })
        product_id = response.json().get("id")

        response = await ac.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json().get("name") == "Another Product"


@pytest.mark.asyncio
async def test_update_product():
    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.post("/products", json={
            "name": "Product to Update",
            "description": "Initial Description",
            "price": 200.0,
            "quantity": 20
        })
        product_id = response.json().get("id")

        response = await ac.put(f"/products/{product_id}", json={
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 250.0,
            "quantity": 15
        })
    assert response.status_code == 200
    assert response.json().get("name") == "Updated Product"
    assert response.json().get("quantity") == 15


@pytest.mark.asyncio
async def test_delete_product():
    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.post("/products", json={
            "name": "Product to Delete",
            "description": "Delete me",
            "price": 50.0,
            "quantity": 5
        })
        product_id = response.json().get("id")
        
        response = await ac.delete(f"/products/{product_id}")
        assert response.status_code == 200

        response = await ac.get(f"/products/{product_id}")
        assert response.status_code == 404


# Тесты для эндпоинтов заказов
@pytest.mark.asyncio
async def test_create_order():
    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.post("/products", json={
            "name": "Product for Order",
            "description": "Available for order",
            "price": 300.0,
            "quantity": 30
        })
        product_id = response.json().get("id")

        response = await ac.post("/orders", json={
            "status": "processing",
            "items": [{"product_id": product_id, "quantity": 5}]
        })
    assert response.status_code == 200
    assert response.json().get("status") == "processing"
    assert response.json().get("items")[0].get("quantity") == 5


@pytest.mark.asyncio
async def test_get_orders():
    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.get("/orders")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_get_order_by_id():
    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.post("/products", json={
            "name": "Product for Another Order",
            "description": "Another available product",
            "price": 400.0,
            "quantity": 50
        })
        product_id = response.json().get("id")

        response = await ac.post("/orders", json={
            "status": "processing",
            "items": [{"product_id": product_id, "quantity": 10}]
        })
        order_id = response.json().get("id")

        response = await ac.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json().get("status") == "processing"
    assert response.json().get("items")[0].get("product_id") == product_id


@pytest.mark.asyncio
async def test_update_order_status():
    async with AsyncClient(base_url=base_url) as ac:
        response = await ac.post("/products", json={
            "name": "Product for Status Update",
            "description": "Ready to be shipped",
            "price": 500.0,
            "quantity": 60
        })
        product_id = response.json().get("id")

        response = await ac.post("/orders", json={
            "status": "processing",
            "items": [{"product_id": product_id, "quantity": 15}]
        })
        order_id = response.json().get("id")

        response = await ac.patch(f"/orders/{order_id}/status", json={"status": "shipped"})
    assert response.status_code == 200
    assert response.json().get("status") == "shipped"
