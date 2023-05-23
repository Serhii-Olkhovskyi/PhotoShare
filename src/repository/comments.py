from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database.models import User, Comment, Role
from src.schemas import CommentBase


async def create_comment(photo_id: int, body: CommentBase, db: Session, user: User) -> Comment:
    new_comment = Comment(text=body.text, photo_id=photo_id, user_id=user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


async def edit_comment(comment_id: int, body: CommentBase, db: Session, user: User) -> Comment | None:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        if user.role in [Role.admin, Role.moderator] or comment.user_id == user.id:
            comment.text = body.text
            comment.updated_at = func.now()
            db.commit()
    return comment


async def delete_comment(comment_id: int, db: Session, user: User) -> None:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment
