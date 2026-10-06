from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

fastapi_app = FastAPI(title="Swaleh AI", version="1.0.0")

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1 import chat
fastapi_app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])

@fastapi_app.get("/")
def root():
    return {"name": "Swaleh AI", "status": "Running", "version": "1.0.0"}

@fastapi_app.get("/health")
def health():
    return {"status": "healthy"}

app = fastapi_app
