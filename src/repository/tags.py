from sqlalchemy.orm import Session

from src.database.models import Tag, User
from src.schemas import TagBase


async def create_tag(body: TagBase, user: User, db: Session) -> Tag:
    tag = db.query(Tag).filter(Tag.title == body.title).first()
    if not tag:
        tag = Tag(title=body.title, user_id=user.id)
        db.add(tag)
        db.commit()
        db.refresh(tag)
    return tag


async def update_tag(tag_id: int, body: TagBase, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.title = body.title
        db.commit()
    return tag


def get_tags(tag_titles: list, user: User, db: Session):

    tags = []
    for tagg_title in tag_titles:
        tag = db.query(Tag).filter(Tag.title == tagg_title).first()
        if not tag:
            tag = Tag(
                title=tagg_title,
                user_id=user.id,
            )
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tags.append(tag)
    return tags
