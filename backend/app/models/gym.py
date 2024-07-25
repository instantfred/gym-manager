from ..database import Base
from sqlalchemy import Column, Integer, Boolean, String

class Gym(Base):
    __tablename__ = 'gyms'

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True)
    name = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    address = Column(String)
    phone_number = Column(String)