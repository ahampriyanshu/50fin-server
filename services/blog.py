from app import model
from app.dto import PostBaseSchema, SinglePostResponse, ListPostResponse
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from slugify import slugify 
from app.database import get_db
from sqlalchemy.exc import IntegrityError


def get_post_service(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    posts = db.query(model.Post).group_by(model.Post.id).filter(
        model.Post.title.contains(search)).limit(limit).offset(skip).all()
    return ListPostResponse(data=posts, metadata={
            'count': len(posts),
            'limit': limit,
            'offset': skip,
    })