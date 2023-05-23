#routes/users.py
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database.db import get_db
from src.schemas import UserResponse, UserProfileModel, RequestEmail, RequestRole
from src.services.auth import auth_service
from src.services.roles import RoleChecker
from src.database.models import Role, User
from src.repository import users as repository_users

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
    Получить всех пользователей

    :param db:
    :return:
    """
    return db.query(User).all()


@router.get("/my/", response_model=UserResponse, tags=['users'])
async def info_my_profile(current_user: User = Depends(auth_service.get_current_user),
                          db: Session = Depends(get_db)):
    """
    Функция возвращает информацию о профиле текущего пользователя.

    :param current_user:
    :param db:
    :return:
    """

    user = await repository_users.get_me(current_user, db)
    return user


@router.put("/edit_me/", response_model=UserResponse, tags=['users'])
async def edit_my_profile(avatar: UploadFile = File(), new_username: str = Form(None),
                          current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Функция edit_my_profile позволяет пользователю редактировать свой профиль.

    :param avatar:
    :param new_username:
    :param current_user:
    :param db:
    :return:
    """

    updated_user = await repository_users.edit_my_profile(avatar, new_username, current_user, db)
    return updated_user


@router.get("/all", response_model=List[UserResponse], dependencies=[Depends(allowed_get_all_users)])
async def read_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Получить всех пользователей

    :param skip:
    :param limit:
    :param db:
    :return:
    """
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/users_with_username/{username}", response_model=List[UserResponse],
            dependencies=[Depends(allowed_get_user)])
async def read_users_by_username(username: str, db: Session = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)):
    """
    Функция используется для чтения пользователей по имени пользователя.

    Возвращается список пользователей с заданным именем пользователя.
    :param username:
    :param db:
    :param current_user:
    :return:
    """

    users = await repository_users.get_users_with_username(username, db)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return users


@router.get("/user_profile_with_username/{username}", response_model=UserProfileModel,
            dependencies=[Depends(allowed_get_user)])
async def read_user_profile_by_username(username: str, db: Session = Depends(get_db),
                                        current_user: User = Depends(auth_service.get_current_user)):
    """
        Функция используется для чтения профиля пользователя по имени пользователя.

        Функция принимает имя пользователя в качестве аргумента и возвращает профиль пользователя, если он существует.
    :param username:
    :param db:
    :param current_user:
    :return:
    """

    user_profile = await repository_users.get_user_profile(username, db)
    if user_profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return user_profile


@router.patch("/ban/{email}/", dependencies=[Depends(allowed_ban_user)])
async def ban_user_by_email(body: RequestEmail, db: Session = Depends(get_db)):
    """
     Функция ban_user_by_email принимает адрес электронной почты пользователя и запрещает пользователю доступ к API.

    Если электронное письмо не найдено в нашей базе данных, создается HTTPException с кодом состояния 401 и
    подробное сообщение «Неверный адрес электронной почты».
    Если пользователь уже был заблокирован, создается HTTPException с кодом состояния 409
    :param body:
    :param db:
    :return:
    """

    user = await repository_users.get_user_by_email(body.email, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID EMAIL")
    if user.is_active:
        await repository_users.ban_user(user.email, db)
        return {"message": "USER NOT ACTIVE"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="USER ALREADY NOT ACTIVE")


@router.patch("/make_role/{email}/", dependencies=[Depends(allowed_change_user_role)])
async def make_role_by_email(body: RequestRole, db: Session = Depends(get_db)):
    """
    Функция используется для изменения роли пользователя.

    Функция принимает адрес электронной почты, роль и изменяет роль пользователя на новую указанную роль.
    Если такого пользователя не существует, то создается HTTPException с кодом состояния 401 (Unauthorized)
    :param body:
    :param db:
    :return:
    """

    user = await repository_users.get_user_by_email(body.email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID EMAIL")
    if body.role == user.role:
        return {"message": "USER ROLE EXISTS"}
    else:
        await repository_users.make_user_role(body.email, body.role, db)
        return {"message": f"USER CHANGE ROLE TO {body.role.value}"}
