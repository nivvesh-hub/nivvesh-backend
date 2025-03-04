from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

class InvestmentPlanSchema(BaseModel):
    id: UUID
    min_years: int
    max_years: int
    min_amount: float
    max_amount: float
    return_rate: float
    title: Optional[str]
    subtitle: Optional[str]

    class Config:
        orm_mode = True

class BankSchema(BaseModel):
    id: UUID
    name: str
    banner: Optional[str]
    icon: Optional[str]
    speciality: Optional[str]
    tags: List[str]
    investmentPlans: List[InvestmentPlanSchema]

    class Config:
        orm_mode = True

class TagResponseSchema(BaseModel):
    type: str
    text: str
    banks: List[BankSchema]
