from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database.models import User, Comment, Role
from src.schemas import CommentBase


async def create_comment(photo_id: int, body: CommentBase, db: Session, user: User) -> Comment:
    """
    The create_comment function creates a new comment in the database.
        Args:
            photo_id (int): The id of the photo to which we are adding a comment.
            body (CommentBase): A CommentBase object containing information about the new comment.
            db (Session): An open database session for querying and modifying data in our database.

    :param photo_id: int: Specify the id of the photo that we want to add a comment to
    :param body: CommentBase: Get the text from the body of the request
    :param db: Session: Access the database
    :param user: User: Get the user_id of the person who is making a comment
    :return: The newly created comment
    """
    new_comment = Comment(text=body.text, photo_id=photo_id, user_id=user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


async def edit_comment(comment_id: int, body: CommentBase, db: Session, user: User) -> Comment | None:
    """
    The edit_comment function takes in a comment_id, body, db and user.
        It then queries the database for the comment with that id. If it exists,
        it checks if the user is an admin or moderator or if they are the owner of
        that particular comment. If so, it updates its text and updated_at fields to
        reflect those changes.

    :param comment_id: int: Identify the comment that is being edited
    :param body: CommentBase: Pass the text of the comment to be edited
    :param db: Session: Access the database
    :param user: User: Check if the user is an admin or moderator,
    :return: A comment or none
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        if user.roles in [Role.admin, Role.moderator] or comment.user_id == user.id:
            comment.text = body.text
            comment.updated_at = func.now()
            db.commit()
    return comment


async def delete_comment(comment_id: int, db: Session, user: User) -> None:
    """
    The delete_comment function deletes a comment from the database.
        Args:
            comment_id (int): The id of the comment to be deleted.
            db (Session): A connection to the database.
            user (User): The user who is deleting this post.

    :param comment_id: int: Specify which comment to delete
    :param db: Session: Pass the database session to the function
    :param user: User: Check if the user is authorized to delete the comment
    :return: The comment that was deleted
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment
