import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.main import app
from src.models import User, Post, Follow, Like, Comment, Notification

TEST_MONGODB_URL = "mongodb://localhost:27017"
TEST_DB_NAME     = "auragram_test"
 
 
@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db():
    client = AsyncIOMotorClient(TEST_MONGODB_URL)
    await init_beanie(
        database=client[TEST_DB_NAME],
        document_models=[User, Post, Follow, Like, Comment, Notification],
    )
    yield
    # Drop test database after all tests
    await client.drop_database(TEST_DB_NAME)
 
 
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


@pytest_asyncio.fixture
async def auth_client():
    """Client with a registered and logged-in user."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        res = await c.post("/api/v1/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        })
        token = res.json()["access_token"]
        c.headers["Authorization"] = f"Bearer {token}"
        yield c
    await User.find(User.email == "test@example.com").delete()