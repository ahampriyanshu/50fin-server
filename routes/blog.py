from sqlalchemy.exc import IntegrityError
from app import model
from services.blog import get_all_posts, create_post, get_post_by_id_or_slug, delete_post_by_id
from app.dto import PostBaseSchema, SinglePostResponse, ListPostResponse, PostResponseSchema
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter
from app.database import get_db
import uuid


router = APIRouter()

@router.get('/', response_model=ListPostResponse)
async def get_posts(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = '') -> ListPostResponse:
    return get_all_posts(db, limit, page, search)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema)
async def create_post(post: PostBaseSchema, db: Session = Depends(get_db)) -> PostResponseSchema:
    return create_post(post, db)


@router.get('/{id_or_slug}', response_model=SinglePostResponse)
async def get_post(id_or_slug: str, db: Session = Depends(get_db)):
    return get_post_by_id_or_slug(id_or_slug, db)


@router.delete('/{id}')
async def delete_post(id: uuid.UUID, db: Session = Depends(get_db)):
    return delete_post_by_id(id, db)