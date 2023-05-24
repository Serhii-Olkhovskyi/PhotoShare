from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from src.database.db import get_db
from src.database.models import User
from src.schemas import PhotoResponse
from src.services.auth import auth_service
from src.schemas_of_transformation import TransformerModel
from src.repository.photo_transformer import transformer, show_qr_code

router = APIRouter(prefix='/transformer', tags=["transformer"])


@router.patch("/{photo_id}", response_model=PhotoResponse, status_code=status.HTTP_200_OK)
async def photo_transform(photo_id: int, body: TransformerModel, db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    """
    The photo_transform function takes a photo_id and a TransformerModel object as input.
    It then calls the transformer function, which returns either an image or None if no image is found.
    If an image is returned, it will be sent back to the client in JSON format.

    :param photo_id: int: Specify the photo id of the image to be transformed
    :param body: TransformerModel: Get the data from the request body
    :param db: Session: Get a database session
    :param current_user: User: Get the current user from the database
    :return: The transformed image
    """
    photo = await transformer(photo_id, body, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')
    return photo


@router.post("/qr_code/{photo_id}", status_code=status.HTTP_201_CREATED)
def show_qr(photo_id: int, db: Session = Depends(get_db),
            current_user: User = Depends(auth_service.get_current_user)):
    """
    The show_qr function takes a photo_id and returns the QR code for that image.
        The function first checks if the user is logged in, then it checks if the photo exists.
        If both of these conditions are met, then it will return a StreamingResponse object containing
        an image/png file with status code 201.

    :param photo_id: int: Specify the id of the photo to be shown
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user that is currently logged in
    :return: A streamingresponse object, which is a subclass of response
    """
    photo = show_qr_code(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')
    return StreamingResponse(photo, media_type="image/png", status_code=status.HTTP_201_CREATED)
