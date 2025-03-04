# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.models import Bank, InvestmentPlan
# from app.schemas import BankSchema, TagResponseSchema
# from app.db.connection import get_db
# from pydantic import BaseModel, constr, conint

# router = APIRouter()


# @router.get("/homepage", response_model=List[TagResponseSchema])
# def get_homepage(tags: str = "MOSTPOPULAR,NEWLYADDED", db: Session = Depends(get_db)):
#     tag_list = tags.split(",")
#     response_data = []

#     for tag in tag_list:
#         banks = db.query(Bank).filter(Bank.tags.contains([tag])).all()

#         def get_bank_data(bank):
#             investment_plans = db.query(InvestmentPlan).filter(InvestmentPlan.bank_id == bank.id).all()
#             return {
#                 "id": bank.id,
#                 "name": bank.name,
#                 "banner": bank.banner,
#                 "icon": bank.icon,
#                 "speciality": bank.speciality,
#                 "tags": [{"key": tag, "value": tag} for tag in bank.tags],
#                 "investmentPlans": [
#                     {
#                         "id": plan.id,
#                         "min_years": plan.min_years,
#                         "max_years": plan.max_years,
#                         "min_amount": plan.min_amount,
#                         "max_amount": plan.max_amount,
#                         "return_rate": plan.return_rate,
#                         "title": plan.title,
#                         "subtitle": plan.subtitle
#                     }
#                     for plan in investment_plans
#                 ]
#             }

#         response_data.append({
#             "type": tag,
#             "text": f"{tag} banks",
#             "banks": [get_bank_data(bank) for bank in banks]
#         })

#     return response_data

