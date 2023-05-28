from app.model import Post
from app.dto import PostBaseSchema, SinglePostResponse, PostResponseSchema, ListPostResponse
from sqlalchemy.orm import Session 
from sqlalchemy import func
from fastapi import Depends, HTTPException, status, Response
from slugify import slugify 
from app.database import get_db
from sqlalchemy.exc import IntegrityError
import uuid


def get_all_posts(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = '') -> ListPostResponse:
    skip = (page - 1) * limit

    count = (
        db.query(func.count(Post.id))
        .filter(Post.title.contains(search))
        .scalar()
    )

    # Retrieve the posts with limit and offset
    posts = (
        db.query(Post)
        .group_by(Post.id)
        .filter(Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return ListPostResponse(
        data=posts,
        metadata={
            'results': count,
            'limit': limit,
            'offset': skip,
        }
    )
    
    
def create_post(post: PostBaseSchema, db: Session = Depends(get_db))  -> PostResponseSchema:
    new_post = Post(**post.dict())
    new_post.slug = slugify(new_post.title)
    new_post.calculate_reading_time()
    db.add(new_post)
    try:
        db.commit()
        db.refresh(new_post)
        return new_post
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Similar title already exists.")
    
    
def get_post_by_id_or_slug(identifier: str, db: Session = Depends(get_db)):
    try:
        identifier_uuid = uuid.UUID(identifier)
        post = db.query(Post).filter(Post.id == identifier_uuid).first()
    except ValueError:
        post = db.query(Post).filter(Post.slug == identifier).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with this identifier found: {identifier}")

    next_post = db.query(Post).filter(Post.id > post.id).order_by(Post.id.asc()).first()
    previous_post = db.query(Post).filter(Post.id < post.id).order_by(Post.id.desc()).first()

    next_post_dict = {
        "id": next_post.id,
        "title": next_post.title,
        "slug": next_post.slug
    } if next_post else None

    previous_post_dict = {
        "id": previous_post.id,
        "title": previous_post.title,
        "slug": previous_post.slug
    } if previous_post else None

    return SinglePostResponse(
        data=post,
        next_post=next_post_dict,
        previous_post=previous_post_dict
    )
       

# @router.put('/{id}', response_model=schemas.PostResponse)
# def update_post(id: str, post: schemas.UpdatePostSchema, db: Session = Depends(get_db), user_id: str = Depends(require_user)):
#     post_query = db.query(Post).filter(Post.id == id)
#     updated_post = post_query.first()

#     if not updated_post:
#         raise HTTPException(status_code=status.HTTP_200_OK,
#                             detail=f'No post with this id: {id} found')
#     if updated_post.user_id != uuid.UUID(user_id):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail='You are not allowed to perform this action')
#     post.user_id = user_id
#     post_query.update(post.dict(exclude_unset=True), synchronize_session=False)
#     db.commit()
#     return updated_post


def delete_post_by_id(id: uuid.UUID, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    # except ValueError:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid UUID')
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No post with this id: {id} found')

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)