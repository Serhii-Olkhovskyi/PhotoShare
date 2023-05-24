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
    """
    The create_comment function creates a new comment for the photo with the given ID.
    The function takes in a CommentBase object, which contains only the body of the comment.
    It then uses this information to create and return a new Comment object.

    :param photo_id: int: Specify the photo that the comment is being created for
    :param body: CommentBase: Validate the request body
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user that is currently logged in
    :return: A comment object
    """
    new_comment = await repository_comments.create_comment(photo_id, body, db, current_user)
    return new_comment


@router.put("/update/{comment_id}", response_model=CommentUpdate, dependencies=[Depends(allowed_update_comments)])
async def update_comment(comment_id: int, body: CommentBase, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_comment function is used to edit a comment.
        The function takes in the comment_id, body and db as parameters.
        It then calls the edit_comment function from repository_comments which returns an edited comment object if successful or None otherwise.
        If it returns None, it raises a 404 error with &quot;COMMENT NOT FOUND&quot; as detail message.

    :param comment_id: int: Specify the comment that is to be deleted
    :param body: CommentBase: Pass the new comment body to the update_comment function
    :param db: Session: Connect to the database
    :param current_user: User: Get the current user
    :return: The edited comment
    """
    edited_comment = await repository_comments.edit_comment(comment_id, body, db, current_user)
    if edited_comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="COMMENT NOT FOUND")
    return edited_comment


@router.delete("/delete/{comment_id}", response_model=CommentModel, dependencies=[Depends(allowed_remove_comments)])
async def delete_comment(comment_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The delete_comment function deletes a comment from the database.
        The function takes in an integer representing the id of the comment to be deleted,
        and returns a dictionary containing information about that comment.

    :param comment_id: int: Get the comment id from the url
    :param db: Session: Get the database session
    :param current_user: User: Check if the user is logged in or not
    :return: A comment object, which is the deleted comment
    """
    deleted_comment = await repository_comments.delete_comment(comment_id, db, current_user)
    if deleted_comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="COMMENT NOT FOUND")
    return deleted_comment
