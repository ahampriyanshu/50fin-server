from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel
import uuid

class PostBaseSchema(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class CreatePostSchema(PostBaseSchema):
    pass

class Metadata(BaseModel):
    count: int
    limit: int
    offset: int

class PostResponseSchema(PostBaseSchema):
    id: uuid.UUID
    slug: str
    reading_time: str
    created_at: datetime
    updated_at: Optional[datetime]
    
class SinglePostResponse(BaseModel):
    data: PostResponseSchema


class UpdatePostSchema(PostResponseSchema):
    id: uuid.UUID
    slug: str
    title: str
    content: str
    category: str
    image: str
    # user_id: uuid.UUID | None = None
    # created_at: datetime | None = None
    # updated_at: datetime | None = None

    class Config:
        orm_mode = True


class ListPostResponse(BaseModel):
    metadata: Optional[Metadata] = None
    data: List[PostResponseSchema]


