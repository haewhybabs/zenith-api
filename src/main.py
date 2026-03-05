from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routes.user import router as user_router
from src.routes.auth import router as auth_router

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

app.include_router(user_router)
app.include_router(auth_router)