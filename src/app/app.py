from fastapi import FastAPI
from .config import Settings
from api.routers import include_routers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(**Settings().app_presets)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
include_routers(app)
