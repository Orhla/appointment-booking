from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.services import router as services_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(services_router)