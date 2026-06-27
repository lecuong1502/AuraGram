from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.database import connect_db
from src.services.upload_service import init_cloudinary
from src.api.v1 import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db(settings.MONGODB_URL, settings.DATABASE_NAME)
    init_cloudinary()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/health")
async def health():
    return {"status": "ok"}