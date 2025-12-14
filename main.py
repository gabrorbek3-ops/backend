from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from app.routers import router
from app.core import store, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await store.start()
    yield
    await store.stop()

app = FastAPI(
    lifespan=lifespan,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()