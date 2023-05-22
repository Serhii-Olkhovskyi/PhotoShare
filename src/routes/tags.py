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
async def create_tag(body: TagBase, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    return await repository_create_tag(body, current_user, db)


@router.put("/update_tag/{tag_id}", response_model=TagResponse, dependencies=[Depends(allowed_edit_hashtag)])
async def update_tag(body: TagBase, tag_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    tag = await repository_update_tag(tag_id, body, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    return tag
