from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config import settings

# 1. The Engine: The actual connection to the database
# We use the DATABASE_URL from our .env via our settings object
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production; True helps you see the SQL in your terminal
)

# 2. The Session Factory: A generator that produces individual database sessions
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevents SQLAlchemy from "forgetting" data after a commit
)

# 3. The Dependency Injection function
async def get_db():
    """
    FastAPI will use this to inject a database session into your routes.
    It ensures the connection is closed automatically after the request.
    """
    async with async_session() as session:
        try:
            yield session
            # We don't call commit here; we let the route handle it
        finally:
            await session.close()