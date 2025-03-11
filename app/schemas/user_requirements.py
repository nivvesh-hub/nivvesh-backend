from pydantic import BaseModel
from uuid import UUID

class RequirementCreate(BaseModel):
    amount: float
    duration: int

    class Config:
        from_attributes = True

# Pydantic Schema for response
class RequirementResponse(RequirementCreate):
    id: UUID
    user_id: UUID
    amount: float
    duration: int

    class Config:
        from_attributes = True
