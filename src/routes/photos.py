from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Request
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
import cloudinary.uploader

from src.conf.config import cloudinary_config
from src.database.db import get_db
from src.database.models import Photo
from src.schemas import PhotoModel, PhotoResponse, PhotoUpdate, PhotoTitleUpdate, PhotoDescriptionUpdate
from src.repository import photos as repository_photos
# from src.services.auth import auth_service

router = APIRouter(prefix='/photos', tags=["photos"])


@router.get("/", response_model=List[PhotoResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def read_contacts(skip: int = 0, limit: int = 25, db: Session = Depends(get_db),):
                        #current_user: User = Depends(auth_service.get_current_user)):
    #photos = await repository_photos.get_photos(skip, limit, current_user, db)
    photos = await repository_photos.get_photos(skip, limit, db)
    return photos


@router.get("/{photo_id}", response_model=PhotoResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def read_contact_id(photo_id: int, db: Session = Depends(get_db),):
                          #current_user: User = Depends(auth_service.get_current_user)):
    #photo = await repository_photos.get_photos_by_id(contact_id, current_user, db)
    photo = await repository_photos.get_photos_by_id(photo_id, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return photo


# @router.get("/search/{information}", response_model=List[ContactResponse],
#             description='No more than 10 requests per minute',
#             dependencies=[Depends(RateLimiter(times=3, seconds=5))])
# async def read_contacts_info(information: str, db: Session = Depends(get_db),
#                              current_user: User = Depends(auth_service.get_current_user)):
#     contact = await repository_contacts.get_contacts_by_info(information, current_user, db)
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
#     return contact


@router.post("/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def create_photo(title, description, db: Session = Depends(get_db), file: UploadFile = File()):
                         # current_user: User = Depends(auth_service.get_current_user)):
    cloudinary_config()
    r = cloudinary.uploader.upload(file.file, public_id=f'PhotoShareApp/"current_user.username"', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'PhotoShareApp/"current_user.username"') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    return await repository_photos.create_photo(title, description, src_url, db)


@router.put("/{photo_id}", response_model=PhotoResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def update_photo(body: PhotoUpdate, photo_id: int, db: Session = Depends(get_db),):
                         #current_user: User = Depends(auth_service.get_current_user)):
    photo = await repository_photos.update_photo(photo_id, body, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return photo


@router.patch("/title/{photo_id}", response_model=PhotoResponse)
async def update_title_photo(body: PhotoTitleUpdate, photo_id: int, db: Session = Depends(get_db)):
    photo = await repository_photos.update_title_photo(photo_id, body, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return photo


@router.patch("/description/{photo_id}", response_model=PhotoResponse)
async def update_description_photo(body: PhotoDescriptionUpdate, photo_id: int, db: Session = Depends(get_db)):
    photo = await repository_photos.update_description_photo(photo_id, body, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return photo


@router.delete("/{photo_id}", response_model=PhotoResponse, description='No more than 10 requests per minute',
               dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def remove_photo(photo_id: int, db: Session = Depends(get_db),):
                         #current_user: User = Depends(auth_service.get_current_user)):
    photo = await repository_photos.remove_photo(photo_id, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return photo
