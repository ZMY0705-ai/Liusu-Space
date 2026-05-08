from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
import uuid
from datetime import datetime

from app import models, schemas
from app.database import get_db
from app.routers.users import get_current_user

router = APIRouter(prefix="/works", tags=["works"])

UPLOAD_DIR = "uploads/covers"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=schemas.WorkResponse)
def create_work(
    work: schemas.WorkCreate, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # 只有is_published=True时才设置published_at（首页可见）
    published_at = datetime.utcnow() if work.is_published else None
    
    db_work = models.Work(
        **work.model_dump(exclude={'is_published'}),  # 排除is_published字段
        author_id=current_user.id,
        published_at=published_at
    )
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work

@router.get("/{work_id}", response_model=schemas.WorkResponse)
def read_work(work_id: int, db: Session = Depends(get_db)):
    from sqlalchemy.orm import joinedload
    work = db.query(models.Work).options(joinedload(models.Work.author)).filter(models.Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")
    
    # Increment view count
    work.view_count += 1
    db.commit()
    db.refresh(work)
    return work

@router.get("/", response_model=List[schemas.WorkResponse])
def list_works(
    skip: int = 0, 
    limit: int = 100, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from sqlalchemy.orm import joinedload
    # 如果用户已登录，返回该用户的status=1作品 + 所有已发表的status=1作品
    # 如果未登录，只返回已发表的status=1作品
    query = db.query(models.Work).options(joinedload(models.Work.author))
    
    if current_user:
        # 已登录：返回该用户的status=1作品（保存+发表） + 其他用户的已发表作品
        query = query.filter(
            ((models.Work.author_id == current_user.id) & (models.Work.status == 1)) | 
            (models.Work.published_at.isnot(None))
        )
    else:
        # 未登录：只返回已发表的作品
        query = query.filter(models.Work.published_at.isnot(None))
    
    works = query.offset(skip).limit(limit).all()
    return works

@router.put("/{work_id}", response_model=schemas.WorkResponse)
def update_work(
    work_id: int, 
    work_update: schemas.WorkUpdate, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    work = db.query(models.Work).filter(models.Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")
    if work.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this work")
    
    # 处理is_published字段
    if work_update.is_published is not None:
        if work_update.is_published and work.published_at is None:
            work.published_at = datetime.utcnow()
        elif not work_update.is_published:
            work.published_at = None
    
    # 更新其他字段
    for field, value in work_update.model_dump(exclude_unset=True, exclude={'is_published'}).items():
        setattr(work, field, value)
    
    db.commit()
    db.refresh(work)
    return work

@router.delete("/{work_id}")
def delete_work(
    work_id: int, 
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    work = db.query(models.Work).filter(models.Work.id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")
    if work.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this work")
    
    # 级联删除关联数据，避免外键约束冲突
    print(f'删除目标 ID: {work_id}')
    print(f'正在删除的作品: {work.title}')
    
    # 1. 删除该作品的所有评论
    db.query(models.WorkComment).filter(models.WorkComment.work_id == work_id).delete()
    
    # 2. 删除该作品的所有点赞记录
    db.query(models.WorkLike).filter(models.WorkLike.work_id == work_id).delete()
    
    # 3. 删除该作品的所有收藏记录
    db.query(models.WorkFavorite).filter(models.WorkFavorite.work_id == work_id).delete()
    
    # 4. 删除作品本身
    db.delete(work)
    db.commit()
    
    print(f'作品 {work_id} 及其关联数据已删除')
    return {"message": "Work deleted successfully"}

@router.post("/upload-cover")
def upload_cover_image(file: UploadFile = File(...)):
    # 生成唯一文件名，防止重名覆盖
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 返回可以通过 /uploads/covers/filename 访问的 URL
    return {"filename": unique_filename, "url": f"/uploads/covers/{unique_filename}"}
