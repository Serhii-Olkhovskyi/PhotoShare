from sqlalchemy import Column, Integer, String, func, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)
    photo_url = Column(String(400))
    qr_code_url = Column(Text, nullable=True)
    title = Column(String(69), nullable=True)
    description = Column(String(777), nullable=True)
    #tags = ...
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    # user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    # user = relationship('User', backref="photos")
