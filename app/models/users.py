from sqlalchemy import Column, Integer, String
from app.db.connection import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4, primary_key=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    age = Column(Integer)
    phone = Column(String, unique=True, nullable=True) 