from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserResponse
from src.services.roles import RoleChecker
from src.database.models import Role, User

router = APIRouter(prefix='/users', tags=["users"])

allowed_get_user = RoleChecker([Role.admin, Role.moderator, Role.user])
allowed_create_user = RoleChecker([Role.admin, Role.moderator, Role.user])
allowed_update_user = RoleChecker([Role.admin, Role.moderator, Role.user])
allowed_get_all_users = RoleChecker([Role.admin])
allowed_remove_user = RoleChecker([Role.admin])
allowed_ban_user = RoleChecker([Role.admin])
allowed_change_user_role = RoleChecker([Role.admin])


@router.get("/users/", response_model=List[UserResponse], tags=['users'])
async def get_users(db: Session = Depends(get_db)):
    """
    Get all users

    :param db:
    :return:
    """
    return db.query(User).all()


@router.get("/users/{user_id}", response_model=List[UserResponse], tags=['users'])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get username user

    :param db:
    :return:
    """
    return db.query(User).filter_by(id == user_id).first()
