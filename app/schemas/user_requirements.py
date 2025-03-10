from pydantic import BaseModel

class RequirementCreate(BaseModel):
    user_id: int
    description: str
    amount: float
    duration: int

    class Config:
        from_attributes = True
