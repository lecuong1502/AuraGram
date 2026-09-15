# backend/tests/test_posts.py
import pytest
import io


def fake_image():
    """Minimal valid PNG bytes for upload tests."""
    return io.BytesIO(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00"
        b"\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18"
        b"\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
    )


@pytest.mark.asyncio
async def test_create_post(auth_client):
    res = await auth_client.post(
        "/api/v1/posts",
        data={"caption": "Hello #world"},
        files=[("files", ("test.png", fake_image(), "image/png"))],
    )
    assert res.status_code == 201
    data = res.json()
    assert data["caption"] == "Hello #world"
    assert "world" in data["hashtags"]
    assert len(data["media"]) == 1


@pytest.mark.asyncio
async def test_create_post_no_files(auth_client):
    res = await auth_client.post("/api/v1/posts", data={"caption": "No image"})
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_get_feed(auth_client):
    res = await auth_client.get("/api/v1/posts/feed")
    assert res.status_code == 200
    data = res.json()
    assert "posts" in data
    assert "has_more" in data


@pytest.mark.asyncio
async def test_get_post(auth_client):
    create = await auth_client.post(
        "/api/v1/posts",
        data={"caption": "Get me"},
        files=[("files", ("img.png", fake_image(), "image/png"))],
    )
    post_id = create.json()["id"]
    res = await auth_client.get(f"/api/v1/posts/{post_id}")
    assert res.status_code == 200
    assert res.json()["id"] == post_id


@pytest.mark.asyncio
async def test_like_post(auth_client):
    create = await auth_client.post(
        "/api/v1/posts",
        data={"caption": "Like me"},
        files=[("files", ("img.png", fake_image(), "image/png"))],
    )
    post_id = create.json()["id"]

    # Like
    res = await auth_client.post(f"/api/v1/posts/{post_id}/like")
    assert res.status_code == 200
    assert res.json()["liked"] is True

    # Unlike
    res = await auth_client.post(f"/api/v1/posts/{post_id}/like")
    assert res.status_code == 200
    assert res.json()["liked"] is False


@pytest.mark.asyncio
async def test_delete_post(auth_client):
    create = await auth_client.post(
        "/api/v1/posts",
        data={"caption": "Delete me"},
        files=[("files", ("img.png", fake_image(), "image/png"))],
    )
    post_id = create.json()["id"]
    res = await auth_client.delete(f"/api/v1/posts/{post_id}")
    assert res.status_code == 204

    res = await auth_client.get(f"/api/v1/posts/{post_id}")
    assert res.status_code == 404