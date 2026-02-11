from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.src.init import init
from server.src.api.routes import router

origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000"   # sometimes React uses this instead
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
