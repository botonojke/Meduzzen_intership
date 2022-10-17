from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from credentials import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), nullable=False, index=True)
    hashed_password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, index=True, unique=True)
    about_user = Column(String(256), index=True)
    register_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
