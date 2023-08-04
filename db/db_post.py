
from routers.schemas import PostBase
from sqlalchemy.orm.session import Session
from db.models import DbPost
import datetime
from fastapi import HTTPException, status

def create(db: Session, request: PostBase):
    new_post = DbPost(
        image_url=request.image_url,
        image_url_type=request.image_url_type,
        caption=request.caption,
        timestamp=datetime.datetime.now(),
        user_id=request.creator_id
        
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

def get_all(db: Session):
    posts = db.query(DbPost).all()
    return posts


def delete(db:Session, id: int, user_id: int):
    post = db.query(DbPost).filter(DbPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with id {user_id} is not authorized to delete this post")
    
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted successfully"}
    