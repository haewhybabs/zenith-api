from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform any startup tasks here
    print("Starting up...")
    yield
    # Perform any shutdown tasks here
    print("Shutting down...")
app = FastAPI(
    title="Zenith API",
    description="A simple API for managing users and items.",
    version="1.0.0",
    lifespan=lifespan
)
@app.get("/")
async def health_check():
    return {"message": "Welcome to Zenith API", "status":"online"}