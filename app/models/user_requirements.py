from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .users import User
Base = declarative_base()

class Requirement(Base):
    __tablename__ = 'requirements'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String)
    amount = Column(Float)  # Amount to invest
    duration = Column(Integer)  # Duration in months (or years, as needed)

    user = relationship("User", back_populates="requirements")

User.requirements = relationship("Requirement", back_populates="user")