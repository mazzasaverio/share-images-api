from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm.session import Session
from routers.schemas import PostBase, PostDisplay
from db.database import get_db
from db.models import DbPost
from db import db_post
import datetime
from typing import List
import random 
import string
import shutil
from routers.schemas import UserAuth
from auth.oauth2 import get_current_user
router = APIRouter(
    prefix="/post",
    tags=["post"],
)

image_url = ["absolute", "realtive"]


@router.post("/")
def create(request: PostBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    new_post = DbPost(
        image_url=request.image_url,
        image_url_type=request.image_url_type,
        caption=request.caption,
        timestamp=datetime.datetime.now(),
        user_id=request.creator_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/all", response_model=list[PostDisplay])
def posts(db: Session = Depends(get_db)):
    return db_post.get_all(db)

@router.post('/image')
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for _ in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'
    
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)
        
        
    return {'filename': path}

@router.get('/delete/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_post.delete_post(id, db)

