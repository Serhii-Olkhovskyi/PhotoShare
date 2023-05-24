from sqlalchemy.orm import Session

from src.database.models import Tag, User
from src.schemas import TagBase


async def create_tag(body: TagBase, user: User, db: Session) -> Tag:
    """
    The create_tag function creates a new tag in the database.

    :param body: TagBase: Pass the request body to the function
    :param user: User: Get the user_id of the tag creator
    :param db: Session: Access the database, and the user: user parameter is used to get the id of
    :return: A new tag
    """
    tag = db.query(Tag).filter(Tag.title == body.title).first()
    if not tag:
        tag = Tag(title=body.title, user_id=user.id)
        db.add(tag)
        db.commit()
        db.refresh(tag)
    return tag


async def update_tag(tag_id: int, body: TagBase, db: Session) -> Tag | None:
    """
    The update_tag function updates a tag in the database.
        Args:
            tag_id (int): The id of the tag to update.
            body (TagBase): The updated information for the specified Tag.

    :param tag_id: int: Specify the tag to be deleted
    :param body: TagBase: Pass the new tag title to the function
    :param db: Session: Pass the database session to the function
    :return: The updated tag
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.title = body.title
        db.commit()
    return tag


def get_tags(tag_titles: list, user: User, db: Session):

    """
    The get_tags function takes a list of tag titles and a user object.
    It then queries the database for each tag title in the list, returning any tags that already exist.
    If no such tags are found, it creates new ones with the given title and user id.

    :param tag_titles: list: Pass in a list of tags that will be used to create the post
    :param user: User: Get the user_id
    :param db: Session: Get the database session
    :return: A list of tags
    """
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
