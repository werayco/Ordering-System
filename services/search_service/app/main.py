from fastapi import FastAPI
from app.routers import search_router
from pyfiglet import Figlet
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    f = Figlet(font='slant')
    print(f.renderText('Auth Service'))
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(search_router)

@app.get("/health")
async def root():
    return {"message": "Welcome to the Search Service", "version": "1.0.0"}