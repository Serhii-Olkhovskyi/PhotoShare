from typing import List

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from src.database.models import Photo, User
from src.schemas import PhotoUpdate, PhotoTitleUpdate, PhotoDescriptionUpdate
from src.repository.tags import get_tags


async def get_photos(skip: int, limit: int, user: User, db: Session) -> List[Photo]:
    """
    The get_photos function returns a list of photos from the database.

    :param skip: int: Skip a certain number of photos
    :param limit: int: Limit the number of photos returned
    :param user: User: Filter the photos by user
    :param db: Session: Access the database
    :return: A list of photo objects
    """
    return db.query(Photo).filter(Photo.user_id == user.id).offset(skip).limit(limit).all()


async def get_photos_by_id(photo_id: int, user: User, db: Session) -> Photo:
    """
    The get_photos_by_id function takes in a photo_id and user, and returns the Photo object with that id.
        Args:
            photo_id (int): The id of the Photo to be returned.
            user (User): The User who owns the Photo to be returned.

    :param photo_id: int: Get the photo by id
    :param user: User: Get the user_id of the photo
    :param db: Session: Pass in a database session to the function
    :return: A single photo by its id and the user who owns it
    """
    return db.query(Photo).filter(and_(Photo.id == photo_id, Photo.user_id == user.id)).first()


async def get_photos_by_info(information: str, user: User, db: Session) -> List[Photo]:
    """
    The get_photos_by_info function takes in a string of information and a user object,
    and returns all photos that match the given information. The function uses the SQLAlchemy ORM to query
    the database for all photos with matching titles or descriptions.

    :param information: str: Search for photos by title or description
    :param user: User: Get the user id of the user who is logged in
    :param db: Session: Access the database
    :return: A list of photos that match the information provided by the user
    """
    return db.query(Photo).filter(Photo.user_id == user.id).filter(or_(Photo.title == information,
                                                                       Photo.description == information,
                                                                       )).all()


async def create_photo(title: str, description: str, tags: List, url, user: User, db: Session) -> Photo:
    """
    The create_photo function creates a new photo in the database.
        Args:
            title (str): The title of the photo.
            description (str): A description of the photo.
            tags (List[str]): A list of tags for this photo, separated by commas and spaces.  For example, &quot;sunset, beach&quot; would be two separate tags for this one image.  This is optional; if no tag is provided then it will default to an empty list [].
            url: The URL where we can find this image on the internet somewhere!  This should be a string that starts

    :param title: str: Specify the title of the photo
    :param description: str: Set the description of the photo
    :param tags: List: Get the tags from the request body
    :param url: Store the url of the photo
    :param user: User: Get the user_id of the photo
    :param db: Session: Create a database session
    :return: A photo object
    """
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


async def update_photo(photo_id: int, body: PhotoUpdate, user: User, db: Session) -> Photo | None:
    """
    The update_photo function updates a photo in the database.
        Args:
            photo_id (int): The id of the photo to update.
            body (PhotoUpdate): The updated information for the Photo object.
            user (User): The User object that is making this request, used to verify ownership of this Photo object.

    :param photo_id: int: Specify the photo to update
    :param body: PhotoUpdate: Pass the data from the request body to update_photo
    :param user: User: Check if the user is authorized to delete a photo
    :param db: Session: Access the database
    :return: A photo or none
    """
    photo = db.query(Photo).filter(and_(Photo.id == photo_id, Photo.user_id == user.id)).first()
    if photo:
        photo.title = body.title
        photo.description = body.description
        db.commit()
    return photo


async def update_title_photo(photo_id: int, body: PhotoTitleUpdate, user: User, db: Session) -> Photo | None:
    """
    The update_title_photo function updates the title of a photo in the database.
        Args:
            photo_id (int): The id of the photo to update.
            body (PhotoTitleUpdate): The new title for this photo.
            user (User): The user who is making this request, used to verify that they own this resource.

    :param photo_id: int: Identify the photo to be updated
    :param body: PhotoTitleUpdate: Pass the title of the photo to be updated
    :param user: User: Ensure that the user is authorized to update the photo
    :param db: Session: Access the database
    :return: The photo object if the update is successful
    """
    photo = db.query(Photo).filter(and_(Photo.id == photo_id, Photo.user_id == user.id)).first()
    if photo:
        photo.title = body.title
        db.commit()
    return photo


async def update_description_photo(photo_id: int, body: PhotoDescriptionUpdate, user: User,
                                   db: Session) -> Photo | None:
    """
    The update_description_photo function updates the description of a photo in the database.
        Args:
            photo_id (int): The id of the photo to update.
            body (PhotoDescriptionUpdate): A PhotoDescriptionUpdate object containing a new description for this photo.
            user (User): The User object representing who is making this request, used to verify ownership of this resource.

    :param photo_id: int: Identify the photo that is being updated
    :param body: PhotoDescriptionUpdate: Get the description from the request body
    :param user: User: Ensure that the user is authorized to update the photo
    :param db: Session: Access the database
    :return: The updated photo
    """
    photo = db.query(Photo).filter(and_(Photo.id == photo_id, Photo.user_id == user.id)).first()
    if photo:
        photo.description = body.description
        db.commit()
    return photo


async def remove_photo(photo_id: int, user: User, db: Session) -> Photo | None:
    """
    The remove_photo function removes a photo from the database.
        Args:
            photo_id (int): The id of the photo to be removed.
            user (User): The user who is removing the photo. This is used for authorization purposes, as only users can remove their own photos.
            db (Session): A session object that allows us to interact with our database and commit changes we make to it.

    :param photo_id: int: Specify the id of the photo to be removed
    :param user: User: Get the user_id from the database
    :param db: Session: Pass the database session to the function
    :return: The photo that was removed, or none if the photo wasn't found
    """
    photo = db.query(Photo).filter(and_(Photo.id == photo_id, Photo.user_id == user.id)).first()
    if photo:
        db.delete(photo)
        db.commit()
    return photo
