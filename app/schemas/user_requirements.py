from pydantic import BaseModel
from typing import Optional

class RequirementBase(BaseModel):
    amount: float
    duration: int  # Duration in months or years

class RequirementCreate(RequirementBase):
    pass

class Requirement(RequirementBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
