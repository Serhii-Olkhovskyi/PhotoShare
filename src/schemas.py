from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int

    class Config:
        orm_mode = True


class PhotoBase(BaseModel):
    photo_url: str = Field(max_length=400, default=None)
    qr_code_url: str = Field(max_length=500, default=None)
    title: str = Field(max_length=69)
    description: str = Field(max_length=777)


class PhotoModel(PhotoBase):
    tags: List[int]

    @validator("tags")
    def validate_tags(cls, tags):
        if len(tags) > 5:
            raise ValueError("Too many tags (MAX 5 tags)")
        return tags


class PhotoUpdate(BaseModel):
    title: str = Field(max_length=69)
    description: str = Field(max_length=777)
    tags: List[int]


class PhotoTitleUpdate(BaseModel):
    title: str = Field(max_length=69)


class PhotoDescriptionUpdate(BaseModel):
    description: str = Field(max_length=777)


class PhotoResponse(PhotoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[TagResponse]

    class Config:
        orm_mode = True
