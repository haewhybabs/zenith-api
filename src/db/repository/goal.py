from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.db.models import Goal
from src.schemas.goal import GoalCreate, GoalUpdate

async def create_new_goal(goal:GoalCreate, db:AsyncSession, onwer_id:int):
   db_goal = Goal(
      **goal.model_dump(),
        owner_id=onwer_id
   )
   db.add(db_goal)
   await db.commit()
   await db.refresh(db_goal)
   return db_goal
async def get_goal_by_id(goal_id:int, db:AsyncSession):
    result = await db.execute(select(Goal).where(Goal.id == goal_id))
    return result.scalars().first()

async def get_all_goals(db: AsyncSession, owner_id: int, skip: int = 0, limit: int = 10):
    # offset() skips the first N items, limit() fetches the next M items
    query = (
        select(Goal)
        .where(Goal.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()

async def update_goal(goal_id:int, goal_data:GoalUpdate, db:AsyncSession, owner_id:int):
    db_goal = await get_goal_by_id(goal_id, db)
    if db_goal and db_goal.owner_id == owner_id:
        for key, value in goal_data.model_dump(exclude_unset=True).items():
            setattr(db_goal, key, value)
        await db.commit()
        await db.refresh(db_goal)
        return db_goal
    return None
async def delete_goal(goal_id:int, db:AsyncSession, owner_id:int):
    db_goal = await get_goal_by_id(goal_id, db)
    if db_goal and db_goal.owner_id == owner_id:
        await db.delete(db_goal)
        await db.commit()
        return True
    return False