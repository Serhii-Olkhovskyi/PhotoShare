from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.repository.tags import create_tag as repository_create_tag
from src.repository.tags import update_tag as repository_update_tag
from src.database.db import get_db
from src.schemas import TagBase, TagResponse
from src.services.roles import RoleChecker
from src.services.auth import auth_service
from src.database.models import Role, User

allowed_edit_hashtag = RoleChecker([Role.admin])

router = APIRouter(prefix='/tags', tags=["tags"])


@router.post("/new/", response_model=TagResponse)
async def create_tag(body: TagBase, current_user: User = Depends(auth_service.get_current_user),
                     db: Session = Depends(get_db)):
    """
    The create_tag function creates a new tag in the database.

    :param body: TagBase: Create a new tag
    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Pass the database session to the repository function
    :return: A tag object
    """
    return await repository_create_tag(body, current_user, db)


@router.put("/update_tag/{tag_id}", response_model=TagResponse, dependencies=[Depends(allowed_edit_hashtag)])
async def update_tag(body: TagBase, tag_id: int, current_user: User = Depends(auth_service.get_current_user),
                     db: Session = Depends(get_db)):
    """
    The update_tag function updates a tag in the database.
        The function takes three arguments:
            body (TagBase): A TagBase object containing the new values for the tag.
            tag_id (int): An integer representing the ID of an existing tag to be updated.
            current_user (User = Depends(auth_service.get_current_user)):
            A User object representing a user who is logged in and has permission to update tags,
            as determined by auth service's get current user function, which checks if there is
            a valid JWT token present in an Authorization header and returns its payload if so;

    :param body: TagBase: Get the data from the request body
    :param tag_id: int: Specify which tag to delete
    :param current_user: User: Get the current user who is logged in
    :param db: Session: Pass the database session to the repository function
    :return: A tag object
    """
    tag = await repository_update_tag(tag_id, body, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    return tag
