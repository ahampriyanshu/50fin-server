from sqlalchemy.exc import IntegrityError
from app import model
from services.blog import get_all_posts, create_post
from app.dto import PostBaseSchema, SinglePostResponse, ListPostResponse, PostResponseSchema
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from app.database import get_db

router = APIRouter()

@router.get('/', response_model=ListPostResponse)
async def get_posts(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = '') -> ListPostResponse:
    return get_all_posts(db, limit, page, search)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema)
async def get_posts(post: PostBaseSchema, db: Session = Depends(get_db)) -> PostResponseSchema:
    return create_post(post, db)



