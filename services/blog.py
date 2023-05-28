from app import model
from app.dto import PostBaseSchema, PostResponseSchema, ListPostResponse
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from slugify import slugify 
from app.database import get_db
from sqlalchemy.exc import IntegrityError


def get_all_posts(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = '') -> ListPostResponse:
    skip = (page - 1) * limit

    posts = db.query(model.Post).group_by(model.Post.id).filter(
        model.Post.title.contains(search)).limit(limit).offset(skip).all()
    return ListPostResponse(data=posts, metadata={
            'count': len(posts),
            'limit': limit,
            'offset': skip,
    })
    

def create_post(post: PostBaseSchema, db: Session = Depends(get_db))  -> PostResponseSchema:
    new_post = model.Post(**post.dict())
    new_post.slug = slugify(new_post.title)
    new_post.calculate_reading_time()
    db.add(new_post)
    try:
        db.commit()
        db.refresh(new_post)
        return new_post
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Title already exists.")