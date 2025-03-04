from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Bank(Base):
    __tablename__ = "banks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    banner = Column(String, nullable=True)  # Store image URLs
    icon = Column(String, nullable=True)  # Store image URLs
    speciality = Column(String(255), nullable=True)
    tags = Column(JSON, nullable=True)  # Store JSON data

class InvestmentPlan(Base):
    __tablename__ = "investment_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bank_id = Column(UUID(as_uuid=True), ForeignKey("banks.id"), nullable=False)
    min_years = Column(Integer, nullable=False)
    max_years = Column(Integer, nullable=False)
    min_amount = Column(DECIMAL(10, 2), nullable=False)
    max_amount = Column(DECIMAL(10, 2), nullable=False)
    return_rate = Column(Float, nullable=False)
    title = Column(String(255), nullable=True)
    subtitle = Column(String(255), nullable=True)
