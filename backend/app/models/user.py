from ..database import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    gym_membership_id = Column(Integer, ForeignKey("gyms.id"))
