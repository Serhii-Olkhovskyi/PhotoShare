import enum
from sqlalchemy import Column, Integer, String, func, ForeignKey, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)
    photo_url = Column(String(400))
    qr_code_url = Column(Text, nullable=True)
    title = Column(String(69), nullable=True)
    description = Column(String(777), nullable=True)
    # tags = ...
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    # user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    # user = relationship('User', backref="photos")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    roles = Column('roles', Enum(Role), default=Role.user)
    created_at = Column('created_at', DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
