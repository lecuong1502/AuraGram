# AuraGram 📸✨

> AI-Powered Social Media Platform — Smart photo sharing with fully local AI features.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18+-61DAFB.svg?logo=react)
![FastAPI](https://img.shields.io/badge/fastapi-0.110+-009688.svg?logo=fastapi)
![MongoDB](https://img.shields.io/badge/mongodb-7.0+-47A248.svg?logo=mongodb)

---

## 📖 Overview

AuraGram is a next-generation photo-sharing app that blends a familiar social media experience with powerful AI features running entirely **locally** — no paid API required. The project is built incrementally, from a solid foundation to advanced AI integrations.

**Highlights:**
- 🤖 Local AI inference on GPU (RTX 4050+), zero API cost
- 🔍 Semantic search — type "beach" and get beach photos even if the caption says nothing
- 🏷️ Auto-tagging and caption/hashtag suggestions from image content
- ⚡ Real-time notifications via WebSocket
- 🎨 AI Stylist: transform photos into anime, sketch, painting styles, and more

---

## 🏗️ Project Structure

```
auragram/
├── frontend/          # React.js (Vite)
├── backend/           # FastAPI
│   ├── api/           # Route handlers
│   ├── models/        # Pydantic schemas
│   ├── services/      # Business logic & AI services
│   └── core/          # Config, DB, Auth
├── ai_models/         # Model weights & inference scripts
├── docker/            # Docker Compose files
└── docs/              # Additional documentation
```

---

## 🛠️ Tech Stack

| Component | Technology | Notes |
|---|---|---|
| Frontend | React.js 18 + Vite | TailwindCSS, React Query |
| Backend | FastAPI (Python 3.11+) | Async, Pydantic v2 |
| Database | MongoDB 7 | Motor (async driver) |
| Auth | JWT (python-jose) | Access + Refresh token |
| File Storage | Cloudinary / MinIO local | Image uploads |
| AI — Caption & Tag | LLaVA / MiniCPM-V (GGUF) | Local inference via llama.cpp |
| AI — Image Style | Stable Diffusion (SDXL-Turbo) | Diffusers + CUDA |
| AI — Semantic Search | CLIP (openai/clip-vit-base) | Embeddings + cosine similarity |
| Real-time | WebSocket (FastAPI native) | Notifications |
| Task Queue | Celery + Redis | Async AI job processing |

> **Minimum GPU requirement:** NVIDIA RTX 4050 6GB VRAM — all models are selected to fit within 6GB.

---

## 🚀 Roadmap

### Phase 1 — Foundation ✅
- [ ] Register / Login (JWT)
- [ ] Post feed (image + caption + like)
- [ ] Image upload to Cloudinary
- [ ] Profile page with photo grid

### Phase 2 — AI Core 🤖
- [ ] **Auto Caption & Hashtag**: Generate captions and hashtags from images using LLaVA
- [ ] **AI Stylist**: Convert photos to anime/sketch styles with SDXL-Turbo

### Phase 3 — Smart Search 🔍
- [ ] **Object Detection**: Auto-tag images on upload (YOLOv8)
- [ ] **Semantic Search**: Find images by natural language description (CLIP embeddings)

### Phase 4 — UX & Real-time ⚡
- [ ] Infinite scroll
- [ ] Real-time notifications (WebSocket)
- [ ] AI Chatbot in messaging

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- MongoDB 7.0
- Redis 7.0
- CUDA 12.x + cuDNN (for AI features)

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/auragram.git
cd auragram
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # Fill in environment variables
uvicorn main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local      # Set VITE_API_URL
npm run dev
```

### 4. Docker Compose (recommended)

```bash
docker compose -f docker/docker-compose.yml up -d
```

### 5. Download AI Models (optional)

```bash
# Automatically downloads model weights to ai_models/weights/
python ai_models/download_models.py --all
```

---

## 🔑 Environment Variables

Create a `.env` file in the `backend/` directory based on `.env.example`:

```env
# App
SECRET_KEY=your-secret-key-here
DEBUG=true

# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=auragram

# Redis (Celery)
REDIS_URL=redis://localhost:6379/0

# File Storage
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# AI (local — no API key needed)
AI_DEVICE=cuda          # or cpu
LLAVA_MODEL_PATH=./ai_models/weights/llava-v1.5-7b.Q4_K_M.gguf
CLIP_MODEL_NAME=openai/clip-vit-base-patch32
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Create a new account |
| POST | `/api/auth/login` | Login and receive JWT |
| GET | `/api/posts/feed` | Get paginated feed |
| POST | `/api/posts` | Create a new post |
| POST | `/api/ai/caption` | Generate caption from image |
| POST | `/api/ai/style-transfer` | Apply AI style to image |
| GET | `/api/search?q={query}` | Semantic image search |

Full API docs: `http://localhost:8000/docs` (Swagger UI, auto-generated)

---

## 🧪 Testing

```bash
# Backend unit tests
cd backend
pytest tests/ -v --cov=.

# Frontend
cd frontend
npm run test
```

---

## 🤝 Contributing

1. Fork this repo
2. Create a new branch: `git checkout -b feat/your-feature-name`
3. Commit your changes: `git commit -m "feat: short description"`
4. Push to the branch: `git push origin feat/your-feature-name`
5. Open a Pull Request and describe what you changed

See [CONTRIBUTING.md](./CONTRIBUTING.md) for full guidelines.

---

## 📋 Commit Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | When to use |
|---|---|
| `feat:` | Add a new feature |
| `fix:` | Fix a bug |
| `docs:` | Update documentation |
| `refactor:` | Refactor code without adding features or fixing bugs |
| `test:` | Add or update tests |
| `chore:` | Config, dependencies |
| `ai:` | AI model or pipeline changes |

---

## 📄 License

Distributed under the [MIT License](./LICENSE).

---

<p align="center">Made with ❤️ by <a href="https://github.com/lecuong1502">Le Kien Cuong</a></p>
