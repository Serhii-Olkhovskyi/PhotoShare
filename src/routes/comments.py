from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import CommentBase, CommentUpdate, CommentModel
from src.repository import comments as repository_comments
from src.services.auth import auth_service
from src.services.roles import RoleChecker
from src.database.models import User, Role

router = APIRouter(prefix='/comments', tags=["comments"])

allowed_get_comments = RoleChecker([Role.admin, Role.moderator, Role.user])
allowed_create_comments = RoleChecker([Role.admin, Role.moderator, Role.user])
allowed_update_comments = RoleChecker([Role.admin, Role.moderator])
allowed_remove_comments = RoleChecker([Role.admin, Role.moderator])


@router.post("/new/{post_id}", response_model=CommentModel, dependencies=[Depends(allowed_create_comments)])
async def create_comment(photo_id: int, body: CommentBase, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    new_comment = await repository_comments.create_comment(photo_id, body, db, current_user)
    return new_comment


@router.put("/update/{comment_id}", response_model=CommentUpdate, dependencies=[Depends(allowed_update_comments)])
async def update_comment(comment_id: int, body: CommentBase, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    edited_comment = await repository_comments.edit_comment(comment_id, body, db, current_user)
    if edited_comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="COMMENT NOT FOUND")
    return edited_comment


@router.delete("/delete/{comment_id}", response_model=CommentModel, dependencies=[Depends(allowed_remove_comments)])
async def delete_comment(comment_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    deleted_comment = await repository_comments.delete_comment(comment_id, db, current_user)
    if deleted_comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="COMMENT NOT FOUND")
    return deleted_comment
