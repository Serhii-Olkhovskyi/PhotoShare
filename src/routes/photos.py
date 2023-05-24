from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Request
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
import cloudinary.uploader

from src.conf.config import cloudinary_config
from src.database.db import get_db
from src.database.models import User
from src.schemas import PhotoResponse, PhotoUpdate, PhotoTitleUpdate, PhotoDescriptionUpdate
from src.repository import photos as repository_photos
from src.services.auth import auth_service


router = APIRouter(prefix='/photos', tags=["photos"])


@router.get("/", response_model=List[PhotoResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def read_photos(skip: int = 0, limit: int = 25, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_photos function returns a list of photos.

    :param skip: int: Skip a number of photos in the database
    :param limit: int: Limit the number of photos returned
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A list of photo objects
    """
    photos = await repository_photos.get_photos(skip, limit, current_user, db)
    return photos


@router.get("/{photo_id}", response_model=PhotoResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def read_photo_id(photo_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_photo_id function is a GET request that returns the photo with the given ID.
    If no such photo exists, it raises an HTTP 404 error.

    :param photo_id: int: Specify the photo id of the image to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A photo object
    """
    photo = await repository_photos.get_photos_by_id(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return photo


@router.get("/search/{information}", response_model=List[PhotoResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def read_photos_info(information: str, db: Session = Depends(get_db),
                           current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_photos_info function will return a photo based on the information provided.
        The function will first check if the user is logged in, and then it will search for a photo with that information.
        If no such photo exists, an HTTP 404 error code is returned.

    :param information: str: Get the information of a photo
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: Information about the photo by id
    """
    contact = await repository_photos.get_photos_by_info(information, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return contact


@router.post("/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def create_photo(title: str, description: str, tags: list, db: Session = Depends(get_db),
                       file: UploadFile = File(),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_photo function creates a new photo in the database.
        It takes in a title, description, and tags for the photo as well as an image file to upload.
        The function then uses Cloudinary's API to upload the image file and return its URL.
        Finally, it returns a JSON response containing information about the newly created photo.

    :param title: str: Set the title of the photo
    :param description: str: Specify the description of the photo
    :param tags: list: Create a list of tags for the photo
    :param db: Session: Pass the database session to the repository function
    :param file: UploadFile: Get the file from the request
    :param current_user: User: Get the current user's username and id
    :return: A photo object
    """
    cloudinary_config()
    r = cloudinary.uploader.upload(file.file, public_id=f'PhotoShareApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'PhotoShareApp/{current_user.username}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    return await repository_photos.create_photo(title, description, tags, src_url, current_user, db)


@router.put("/{photo_id}", response_model=PhotoResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def update_photo(body: PhotoUpdate, photo_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_photo function updates a photo in the database.
        The function takes three arguments:
            - body: A PhotoUpdate object containing the new values for the photo's fields.
            - photo_id: An integer representing the ID of an existing image in our database.
                This is used to identify which image we want to update, and it is passed as a path parameter by FastAPI.
                We use this value to query our database for an existing record with that ID, and if one exists, we update its fields with those provided by body (the PhotoUpdate object). If no such record exists, then

    :param body: PhotoUpdate: Get the information from the request body
    :param photo_id: int: Specify the id of the photo to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A photo object
    """
    photo = await repository_photos.update_photo(photo_id, body, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return photo


@router.patch("/title/{photo_id}", response_model=PhotoResponse)
async def update_title_photo(body: PhotoTitleUpdate, photo_id: int, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_title_photo function updates the title of a photo.
        The function takes in a PhotoTitleUpdate object, which contains the new title for the photo.
        It also takes in an integer representing the id of the photo to be updated and two optional parameters:
            - db: A database session that is used to query data from our database (defaults to Depends(get_db))
            - current_user: An instance of User containing information about our currently logged-in user (defaults to Depends(auth_service.get_current_user))

    :param body: PhotoTitleUpdate: Get the new title from the request body
    :param photo_id: int: Get the photo id from the url
    :param db: Session: Access the database
    :param current_user: User: Get the current user
    :return: The updated photo object
    """
    photo = await repository_photos.update_title_photo(photo_id, body, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return photo


@router.patch("/description/{photo_id}", response_model=PhotoResponse)
async def update_description_photo(body: PhotoDescriptionUpdate, photo_id: int, db: Session = Depends(get_db),
                                   current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_description_photo function updates the description of a photo.
        The function takes in a PhotoDescriptionUpdate object, which contains the new description for the photo.
        It also takes in an integer representing the id of the photo to be updated and two optional parameters:
            - db: Session = Depends(get_db) is used to access our database using SQLAlchemy's session object.
                This parameter is optional because it has a default value (Depends(get_db)) that will be used if no value is passed into this parameter when calling update_description_photo().

    :param body: PhotoDescriptionUpdate: Get the description from the request body
    :param photo_id: int: Identify the photo that is being updated
    :param db: Session: Access the database
    :param current_user: User: Check if the user is logged in
    :return: A photo object
    """
    photo = await repository_photos.update_description_photo(photo_id, body, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return photo


@router.delete("/{photo_id}", response_model=PhotoResponse, description='No more than 10 requests per minute',
               dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def remove_photo(photo_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_photo function removes a photo from the database.
        The function takes in an integer representing the id of the photo to be removed,
        and returns a dictionary containing information about that image.

    :param photo_id: int: Specify the id of the photo to be removed
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user and check if they are authorized to delete the image
    :return: A photo object
    """
    photo = await repository_photos.remove_photo(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return photo
