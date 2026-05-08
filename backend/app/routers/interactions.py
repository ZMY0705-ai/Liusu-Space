from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db
from app.routers.users import get_current_user

router = APIRouter(tags=["interactions"])

# --- Work Comments ---
@router.post("/works/{work_id}/comments")
def add_work_comment(
    work_id: int, 
    comment: schemas.WorkCommentCreate, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    work = db.query(models.Work).filter(models.Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")
    
    # 如果指定了parent_id，验证父评论是否存在
    if comment.parent_id:
        parent_comment = db.query(models.WorkComment).filter(
            models.WorkComment.id == comment.parent_id,
            models.WorkComment.work_id == work_id
        ).first()
        if not parent_comment:
            raise HTTPException(status_code=404, detail="Parent comment not found")
    
    db_comment = models.WorkComment(
        content=comment.content,
        work_id=work_id,
        user_id=current_user.id,
        parent_id=comment.parent_id
    )
    db.add(db_comment)
    
    # Update count
    work.comment_count += 1
    
    # Create notification
    if work.author_id != current_user.id:
        notification = models.Notification(
            user_id=work.author_id,
            type="comment",
            sender_id=current_user.id,
            target_type="work",
            target_id=work_id,
            content=f"{current_user.nickname} 评论了你的作品"
        )
        db.add(notification)
        
    db.commit()
    db.refresh(db_comment)
    return {"message": "Comment added", "comment_id": db_comment.id}

@router.get("/works/{work_id}/comments")
def list_work_comments(work_id: int, db: Session = Depends(get_db)):
    from sqlalchemy.orm import joinedload
    
    # 获取所有评论（包括用户信息）
    comments = db.query(models.WorkComment).options(
        joinedload(models.WorkComment.user)
    ).filter(
        models.WorkComment.work_id == work_id
    ).all()
    
    # 构建树形结构
    def build_comment_tree(comments_list, parent_id=None):
        tree = []
        for comment in comments_list:
            if comment.parent_id == parent_id:
                comment_dict = {
                    "id": comment.id,
                    "work_id": comment.work_id,
                    "user_id": comment.user_id,
                    "content": comment.content,
                    "parent_id": comment.parent_id,
                    "created_at": comment.created_at,
                    "user": {
                        "id": comment.user.id,
                        "account": comment.user.account,
                        "nickname": comment.user.nickname,
                        "avatar": comment.user.avatar,
                        "signature": comment.user.signature,
                        "bio": comment.user.bio,
                        "real_name": comment.user.real_name,
                        "student_id": comment.user.student_id,
                        "major": comment.user.major,
                        "is_real_name_public": bool(comment.user.is_real_name_public),
                        "is_major_public": bool(comment.user.is_major_public)
                    } if comment.user else None,
                    "replies": build_comment_tree(comments_list, comment.id)
                }
                tree.append(comment_dict)
        return tree
    
    # 只返回顶级评论（parent_id为None）
    return build_comment_tree(comments, parent_id=None)

# --- Work Likes ---
@router.post("/works/{work_id}/like")
def like_work(
    work_id: int, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    work = db.query(models.Work).filter(models.Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")
    
    existing_like = db.query(models.WorkLike).filter(
        models.WorkLike.work_id == work_id,
        models.WorkLike.user_id == current_user.id
    ).first()
    
    if existing_like:
        db.delete(existing_like)
        work.like_count -= 1
    else:
        db_like = models.WorkLike(work_id=work_id, user_id=current_user.id)
        db.add(db_like)
        work.like_count += 1
        
        # Create notification
        if work.author_id != current_user.id:
            notification = models.Notification(
                user_id=work.author_id,
                type="like",
                sender_id=current_user.id,
                target_type="work",
                target_id=work_id,
                content=f"{current_user.nickname} 点赞了你的作品"
            )
            db.add(notification)
            
    db.commit()
    return {"message": "Like status updated", "count": work.like_count}

# --- Work Favorites ---
@router.post("/works/{work_id}/favorite")
def favorite_work(
    work_id: int, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    work = db.query(models.Work).filter(models.Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")
    
    existing_fav = db.query(models.WorkFavorite).filter(
        models.WorkFavorite.work_id == work_id,
        models.WorkFavorite.user_id == current_user.id
    ).first()
    
    if existing_fav:
        db.delete(existing_fav)
        work.favorite_count -= 1
    else:
        db_fav = models.WorkFavorite(work_id=work_id, user_id=current_user.id)
        db.add(db_fav)
        work.favorite_count += 1
        
        # Create notification
        if work.author_id != current_user.id:
            notification = models.Notification(
                user_id=work.author_id,
                type="favorite",
                sender_id=current_user.id,
                target_type="work",
                target_id=work_id,
                content=f"{current_user.nickname} 收藏了你的作品"
            )
            db.add(notification)
            
    db.commit()
    return {"message": "Favorite status updated", "count": work.favorite_count}

# --- Get User Interaction Status ---
@router.get("/works/{work_id}/interaction-status")
def get_interaction_status(
    work_id: int, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    work = db.query(models.Work).filter(models.Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")
    
    is_liked = db.query(models.WorkLike).filter(
        models.WorkLike.work_id == work_id,
        models.WorkLike.user_id == current_user.id
    ).first() is not None
    
    is_favorited = db.query(models.WorkFavorite).filter(
        models.WorkFavorite.work_id == work_id,
        models.WorkFavorite.user_id == current_user.id
    ).first() is not None
    
    return {
        "is_liked": is_liked,
        "is_favorited": is_favorited,
        "like_count": work.like_count,
        "favorite_count": work.favorite_count
    }

# --- Get User's Favorites ---
@router.get("/favorites")
def get_my_favorites(
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    from sqlalchemy.orm import joinedload
    favorites = db.query(models.WorkFavorite).filter(
        models.WorkFavorite.user_id == current_user.id
    ).all()
    
    # 获取收藏的作品详情
    work_ids = [fav.work_id for fav in favorites]
    works = db.query(models.Work).options(
        joinedload(models.Work.author)
    ).filter(
        models.Work.id.in_(work_ids)
    ).all()
    
    return works
