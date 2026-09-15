# backend/tests/test_auth.py
import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    res = await client.post("/api/v1/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123",
    })
    assert res.status_code == 201
    data = res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {"username": "user1", "email": "dup@example.com", "password": "password123"}
    await client.post("/api/v1/auth/register", json=payload)
    res = await client.post("/api/v1/auth/register", json={**payload, "username": "user2"})
    assert res.status_code == 409


@pytest.mark.asyncio
async def test_register_duplicate_username(client):
    payload = {"username": "dupuser", "email": "a@example.com", "password": "password123"}
    await client.post("/api/v1/auth/register", json=payload)
    res = await client.post("/api/v1/auth/register", json={**payload, "email": "b@example.com"})
    assert res.status_code == 409


@pytest.mark.asyncio
async def test_register_invalid_username(client):
    res = await client.post("/api/v1/auth/register", json={
        "username": "ab",  # too short
        "email": "x@example.com",
        "password": "password123",
    })
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_register_short_password(client):
    res = await client.post("/api/v1/auth/register", json={
        "username": "validuser",
        "email": "x@example.com",
        "password": "short",
    })
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/api/v1/auth/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "password123",
    })
    res = await client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "password123",
    })
    assert res.status_code == 200
    assert "access_token" in res.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    res = await client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "wrongpassword",
    })
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client):
    reg = await client.post("/api/v1/auth/register", json={
        "username": "refreshuser",
        "email": "refresh@example.com",
        "password": "password123",
    })
    refresh_token = reg.json()["refresh_token"]
    res = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert res.status_code == 200
    assert "access_token" in res.json()


@pytest.mark.asyncio
async def test_get_me(auth_client):
    res = await auth_client.get("/api/v1/users/me")
    assert res.status_code == 200
    data = res.json()
    assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_me_unauthorized(client):
    res = await client.get("/api/v1/users/me")
    assert res.status_code == 403