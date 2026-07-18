from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def root():
    return {"message": "Welcome to screenbond", "version": "1.0.0"}