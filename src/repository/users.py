from typing import List

import cloudinary
from sqlalchemy import func

from sqlalchemy.orm import Session
from libgravatar import Gravatar

from src.conf.config import cloudinary_config
from src.database.models import User, Role
from src.schemas import UserModel, UserProfileModel


async def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter_by(email=email).first()


async def create_user(body: UserModel, db: Session):
    g = Gravatar(body.email)
    g.get_image()

    new_user = User(**body.dict(), avatar=g.get_image())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, refresh_token, db: Session):
    user.refresh_token = refresh_token
    db.commit()


async def get_me(user: User, db: Session) -> User:
    """
    Получение текущего пользователя

    :param user:
    :param db:
    :return:
    """

    user = db.query(User).filter(User.id == user.id).first()
    return user


async def edit_my_profile(file, new_username, user: User, db: Session) -> User:
    """
    Редактирование профиля пользователя

    :param file:
    :param new_username:
    :param user:
    :param db:
    :return:
    """

    me = db.query(User).filter(User.id == user.id).first()
    if new_username:
        me.username = new_username

    cloudinary_config()
    cloudinary.uploader.upload(file.file, public_id=f'Photoshare/{me.username}',
                               overwrite=True, invalidate=True)
    url = cloudinary.CloudinaryImage(f'Photoshare/{me.username}') \
        .build_url(width=250, height=250, crop='fill')
    me.avatar = url
    db.commit()
    db.refresh(me)
    return me


async def get_users(skip: int, limit: int, db: Session) -> List[User]:
    """
    Получение списка пользователей

    :param skip:
    :param limit:
    :param db:
    :return:
    """

    return db.query(User).offset(skip).limit(limit).all()


async def get_users_with_username(username: str, db: Session) -> List[User]:
    """
    Получение списка пользователей по имени

    :param username:
    :param db:
    :return:
    """

    return db.query(User).filter(User.username.ilike(f'%{username}%')).all()


async def get_user_profile(username: str, db: Session) -> User:
    """
    Получение профиля пользователя по имени

    :param username:
    :param db:
    :return:
    """

    user = db.query(User).filter(User.username == username).first()
    if user:
        user_profile = UserProfileModel(
            username=user.username,
            email=user.email,
            avatar=user.avatar,
            created_at=user.created_at,
            is_active=user.is_active
        )
        return user_profile
    return None


async def ban_user(email: str, db: Session) -> None:
    """
    Забанить пользователя

    :param email:
    :param db:
    :return:
    """

    user = db.query(User).filter(User.email == email).first()
    if user:
        user.is_active = False
        db.commit()
        db.refresh(user)
        return user
    return None


async def make_user_role(email: str, role: Role, db: Session) -> None:
    """
    Изменить роль пользователю

    :param email:
    :param role:
    :param db:
    :return:
    """

    user = await get_user_by_email(email, db)
    user.role = role
    db.commit()
