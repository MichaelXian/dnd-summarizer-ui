from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.src.init import init
from server.src.api.routes import router

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init()

app.include_router(router)
