from sqlalchemy.exc import IntegrityError
from app import model
from services.blog import get_post_service
from app.dto import PostBaseSchema, SinglePostResponse, ListPostResponse
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from app.database import get_db

router = APIRouter()

@router.get('/', response_model=ListPostResponse)
async def get_posts(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = '') -> ListPostResponse:
    return get_post_service(db, limit, page, search)


def get_posts(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    posts = db.query(model.Post).group_by(model.Post.id).filter(
        model.Post.title.contains(search)).limit(limit).offset(skip).all()
    return ListPostResponse(data=posts, metadata={
            'count': len(posts),
            'limit': limit,
            'offset': skip,
    })


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=SinglePostResponse)
def create_post(post: PostBaseSchema, db: Session = Depends(get_db)):
    new_post = model.Post(**post.dict())
    new_post.slug = slugify(new_post.title)  # Generate slug from title
    db.add(new_post)
    try:
        db.commit()
        db.refresh(new_post)
        return SinglePostResponse(data=new_post)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Title already exists.")



