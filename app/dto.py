from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import uuid


class PostBaseSchema(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class Metadata(BaseModel):
    results: int
    limit: int
    offset: int


class PostResponseSchema(PostBaseSchema):
    id: uuid.UUID
    slug: str
    created_at: datetime
    updated_at: Optional[datetime]


class SinglePostResponse(BaseModel):
    data: PostResponseSchema
    previous_post: Optional[dict] = None
    next_post: Optional[dict] = None


class UpdatePostSchema(BaseModel):
    title: Optional[str]
    body: Optional[str]


class ListPostResponse(BaseModel):
    metadata: Optional[Metadata] = None
    data: List[PostResponseSchema]
