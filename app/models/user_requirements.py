from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .users import User
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Requirement(Base):
    __tablename__ = 'requirements'
    id = Column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4, primary_key=True)
    user_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    amount = Column(Float)  # Amount to invest
    duration = Column(Integer)  # Duration in months (or years, as needed)

    # user = relationship("User", back_populates="requirements")

