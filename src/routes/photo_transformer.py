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
    photo = await transformer(photo_id, body, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')
    return photo


@router.post("/qr_code/{photo_id}", status_code=status.HTTP_201_CREATED)
def show_qr(photo_id: int, db: Session = Depends(get_db),
            current_user: User = Depends(auth_service.get_current_user)):
    photo = show_qr_code(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')
    return StreamingResponse(photo, media_type="image/png", status_code=status.HTTP_201_CREATED)
