import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, items

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    default_response = {
    'status': True,
    'msg': ''
}
    return default_response


app.include_router(users.router)
app.include_router(items.router)

