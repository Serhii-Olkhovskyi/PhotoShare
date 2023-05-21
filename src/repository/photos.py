from typing import List
from datetime import datetime, timedelta

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from src.database.models import Photo, User
from src.schemas import PhotoModel, PhotoUpdate, PhotoTitleUpdate, PhotoDescriptionUpdate
from src.repository.tags import get_tags

async def get_photos(skip: int, limit: int, db: Session) -> List[Photo]:
    #return db.query(Photo).filter(Photo.user_id == user.id).offset(skip).limit(limit).all()
    return db.query(Photo).offset(skip).limit(limit).all()


async def get_photos_by_id(photo_id: int, db: Session) -> Photo:
    #return db.query(Photo).filter(and_(Photo.id == photo_id, Photo.user_id == user.id)).first()
    return db.query(Photo).filter(Photo.id == photo_id).first()

#async def get_photos_by_info(information: str, db: Session) -> List[Photo]:
    #return db.query(Photo).filter(Contact.user_id == user.id).filter(or_(Photo.firstname == information,
    #                                                                       Photo.lastname == information,
    #                                                                       Photo.email == information, )).all()


async def create_photo(title: str, description: str, tags: List, url, user: User, db: Session) -> Photo:
    if tags:
        tags = get_tags(tags[0].split(","), user, db)
    photo = Photo(
        photo_url=url,
        title=title,
        description=description,
        tags=tags,
        user_id=user.id
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


async def update_photo(photo_id: int, body: PhotoUpdate, db: Session) -> Photo | None:
    #contact = db.query(Photo).filter(and_(Photo.id == photo_id, Photo.user_id == user.id)).first()
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo:
        photo.title = body.title
        photo.description = body.description
        db.commit()
    return photo


async def update_title_photo(photo_id: int, body: PhotoTitleUpdate, db: Session) -> Photo | None:
    #contact = db.query(Photo).filter(and_(Photo.id == photo_id, Photo.user_id == user.id)).first()
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo:
        photo.title = body.title
        db.commit()
    return photo


async def update_description_photo(photo_id: int, body: PhotoDescriptionUpdate, db: Session) -> Photo | None:
    #contact = db.query(Photo).filter(and_(Photo.id == photo_id, Photo.user_id == user.id)).first()
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo:
        photo.description = body.description
        db.commit()
    return photo


async def remove_photo(photo_id: int, db: Session) -> Photo | None:
    #photo = db.query(Photo).filter(and_(Photo.id == photo_id, Photo.user_id == user.id)).first()
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo:
        db.delete(photo)
        db.commit()
    return photo
