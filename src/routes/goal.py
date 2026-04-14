from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.db.session import get_db
from src.db.models import User
from src.schemas.goal import GoalCreate, GoalResponse, GoalUpdate
from src.db.repository.goal import (
    create_new_goal, 
    get_goal_by_id, 
    get_all_goals, 
    update_goal, 
    delete_goal
)
from src.auth.dependencies import get_current_user

router = APIRouter(prefix="/goals", tags=["goals"])

@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal_endpoint(
    goal: GoalCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_new_goal(goal, db, current_user.id)
@router.get("/", response_model=List[GoalResponse])
async def read_goals_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=100) 
):
    # Pass the new parameters to the repository
    return await get_all_goals(
        db=db, 
        owner_id=current_user.id, 
        skip=skip, 
        limit=limit
    )

@router.get("/{goal_id}", response_model=GoalResponse)
async def read_goal_endpoint(
    goal_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = await get_goal_by_id(goal_id, db)
    if not goal or goal.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return goal
@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal_endpoint(
    goal_id: int,
    goal_data: GoalUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_goal = await update_goal(goal_id, goal_data, db, owner_id=current_user.id)
    if not updated_goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found or not owned by user")
    return updated_goal

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal_endpoint(
    goal_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await delete_goal(goal_id, db, owner_id=current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found or not owned by user")
