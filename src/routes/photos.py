from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
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


@router.post("/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def create_photo(body: PhotoModel, db: Session = Depends(get_db), file: UploadFile = File()):
                         # current_user: User = Depends(auth_service.get_current_user)):
    cloudinary_config()
    r = cloudinary.uploader.upload(file.file, public_id=f'PhotoShareApp/"current_user.username"', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'PhotoShareApp/{"current_user.username"}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    return await repository_photos.create_photo(body, src_url, db)


@router.put("/{photo_id}", response_model=PhotoResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def update_photo(body: PhotoUpdate, photo_id: int, db: Session = Depends(get_db),):
                         #current_user: User = Depends(auth_service.get_current_user)):
    photo = await repository_photos.update_photo(photo_id, body, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return photo


@router.patch("/{photo_id}", response_model=PhotoResponse)
async def update_title_photo(body: PhotoTitleUpdate, photo_id: int, db: Session = Depends(get_db)):
    photo = await repository_photos.update_title_photo(photo_id, body, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return photo


@router.patch("/{photo_id}", response_model=PhotoResponse)
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
