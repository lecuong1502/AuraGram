# AuraGram Backend

FastAPI + MongoDB (Beanie ODM) backend for **AuraGram** — a social photo-sharing app.

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.115 |
| Database | MongoDB 7 via Motor + Beanie |
| Auth | JWT (access + refresh token rotation) |
| Storage | Cloudinary |
| Task queue | Celery + Redis *(Phase 2)* |
| AI inference | LLaVA / CLIP / YOLOv8 *(Phase 3)* |

## Quick Start

```bash
# 1. Copy env
cp .env.example .env
# Fill in SECRET_KEY and CLOUDINARY_* values

# 2. Run with Docker Compose (includes MongoDB + Redis)
docker compose up --build

# — OR — run locally
pip install -r requirements.txt
uvicorn main:app --reload
```

Server starts at **http://localhost:8000**  
Interactive docs: **http://localhost:8000/docs**

## Project Structure

```
backend/
├── main.py                  # FastAPI app, middleware, lifespan
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── src/
    ├── api/v1/              # Route handlers
    │   ├── auth.py          # POST /auth/register, /login, /refresh, /logout
    │   ├── users.py         # GET/PATCH /users/me, follow, followers, following
    │   ├── posts.py         # CRUD posts, like, archive
    │   ├── comments.py      # CRUD comments, replies, pin
    │   ├── notifications.py # GET /notifications, mark-all-read
    │   ├── search.py        # GET /search/posts, /search/users, /search/explore
    │   └── upload.py        # POST /upload/image
    ├── core/
    │   ├── config.py        # Pydantic settings (reads .env)
    │   ├── database.py      # Beanie init
    │   ├── security.py      # JWT helpers
    │   ├── dependencies.py  # get_current_user FastAPI dependency
    │   └── logging.py       # Structured logging setup
    ├── models/              # Beanie Document models (MongoDB collections)
    │   ├── user.py          # User (bcrypt, text index, counters)
    │   ├── post.py          # Post + MediaItem + Location
    │   ├── comment.py       # Comment + embedded Reply
    │   ├── like.py          # Like
    │   ├── follow.py        # Follow (pending / accepted)
    │   └── notification.py  # Notification (TTL 90 days, dedup index)
    ├── schemas/             # Pydantic request/response models
    └── services/            # Business logic
        ├── auth_service.py  # register, login, refresh, logout
        ├── user_service.py  # profile, follow/unfollow, followers, search
        ├── post_service.py  # CRUD, feed, explore, search, archive, like
        ├── comment_service.py # CRUD comments/replies, pin
        ├── notification_service.py # push, list, mark-read
        └── upload_service.py   # Cloudinary upload/delete
```

## API Overview

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/auth/register` | ✗ | Create account |
| POST | `/api/v1/auth/login` | ✗ | Get tokens |
| POST | `/api/v1/auth/refresh` | ✗ | Rotate refresh token |
| POST | `/api/v1/auth/logout` | ✓ | Revoke refresh token |
| GET | `/api/v1/users/me` | ✓ | Current user profile |
| PATCH | `/api/v1/users/me` | ✓ | Update profile |
| POST | `/api/v1/users/me/avatar` | ✓ | Upload avatar |
| GET | `/api/v1/users/{username}` | ✗ | Public profile |
| GET | `/api/v1/users/{id}/posts` | ✗ | Profile grid |
| GET | `/api/v1/users/{id}/followers` | ✓ | Followers list |
| GET | `/api/v1/users/{id}/following` | ✓ | Following list |
| POST | `/api/v1/users/{id}/follow` | ✓ | Follow user |
| DELETE | `/api/v1/users/{id}/follow` | ✓ | Unfollow user |
| GET | `/api/v1/posts/feed` | ✓ | Followed users feed |
| POST | `/api/v1/posts` | ✓ | Create post |
| GET | `/api/v1/posts/{id}` | ✗ | Get post |
| DELETE | `/api/v1/posts/{id}` | ✓ | Delete post |
| POST | `/api/v1/posts/{id}/like` | ✓ | Toggle like |
| PATCH | `/api/v1/posts/{id}/archive` | ✓ | Toggle archive |
| GET | `/api/v1/posts/{id}/comments` | ✗ | List comments |
| POST | `/api/v1/posts/{id}/comments` | ✓ | Add comment |
| DELETE | `/api/v1/posts/{id}/comments/{cid}` | ✓ | Delete comment |
| POST | `/api/v1/posts/{id}/comments/{cid}/replies` | ✓ | Reply to comment |
| POST | `/api/v1/posts/{id}/comments/{cid}/pin` | ✓ | Toggle pin comment |
| GET | `/api/v1/notifications` | ✓ | List notifications |
| POST | `/api/v1/notifications/read-all` | ✓ | Mark all read |
| GET | `/api/v1/search/posts` | ✓ | Search by hashtag/keyword |
| GET | `/api/v1/search/users` | ✓ | Search users |
| GET | `/api/v1/search/explore` | ✓ | Explore feed |
| POST | `/api/v1/upload/image` | ✓ | Pre-upload image |

## Running Tests

```bash
pytest tests/ -v
```
