from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db
from app.routers.users import get_current_user

router = APIRouter(prefix="/forum", tags=["forum"])

@router.post("/posts", response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostCreate, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    db_post = models.ForumPost(
        **post.model_dump(),
        author_id=current_user.id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/posts", response_model=List[schemas.PostResponse])
def list_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    from sqlalchemy.orm import joinedload
    posts = db.query(models.ForumPost).options(joinedload(models.ForumPost.author)).offset(skip).limit(limit).all()
    return posts

@router.get("/posts/{post_id}", response_model=schemas.PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    from sqlalchemy.orm import joinedload
    post = db.query(models.ForumPost).options(joinedload(models.ForumPost.author)).filter(models.ForumPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/posts/{post_id}/comments")
def add_post_comment(
    post_id: int, 
    comment: schemas.PostCommentCreate, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    post = db.query(models.ForumPost).filter(models.ForumPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = models.PostComment(
        content=comment.content,
        post_id=post_id,
        user_id=current_user.id,
        parent_id=comment.parent_id
    )
    db.add(db_comment)
    
    # Update count
    post.comment_count += 1
    
    # Create notification
    if post.author_id != current_user.id:
        notification = models.Notification(
            user_id=post.author_id,
            type="reply",
            sender_id=current_user.id,
            target_type="post",
            target_id=post_id,
            content=f"{current_user.nickname} 回复了你的帖子"
        )
        db.add(notification)
        
    db.commit()
    return {"message": "Comment added"}

@router.get("/posts/{post_id}/comments")
def list_post_comments(post_id: int, db: Session = Depends(get_db)):
    from sqlalchemy.orm import joinedload
    comments = db.query(models.PostComment).options(joinedload(models.PostComment.user)).filter(models.PostComment.post_id == post_id).all()
    return comments
