from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_  # Import 'or_' for the flexible check
from src.db.session import get_db
from src.db.models import User
from src.auth.utils import verify_password
from src.auth.jwt import create_access_token

router = APIRouter(tags=["Authentication"])

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    # 1. Search for the user by Username OR Email
    # form_data.username is just the label for the 'identifier' field
    query = select(User).where(
        or_(
            User.username == form_data.username, 
            User.email == form_data.username
        )
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    # 2. Verify existence and password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Create the JWT Token
    # We use the unique email as the 'sub' (subject) claim
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}