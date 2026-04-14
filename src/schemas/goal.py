from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: Optional[bool] = False
    target_date: Optional[datetime] = None

class GoalCreate(GoalBase):
    pass

class GoalUpdate(GoalBase):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    target_date: Optional[datetime] = None

class GoalResponse(GoalBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)