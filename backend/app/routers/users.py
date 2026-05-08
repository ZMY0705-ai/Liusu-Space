from fastapi import APIRouter, Depends, HTTPException, status, Header, UploadFile, File
from sqlalchemy.orm import Session
from app import models, schemas, security
from app.database import get_db
from jose import JWTError
import os
import uuid
from pathlib import Path

router = APIRouter(prefix="/users", tags=["users"])

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    print(f'\n[认证检查] Authorization header: {authorization}')
    
    if authorization is None:
        print('[认证失败] 缺少 Authorization header')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    scheme, _, token = authorization.partition(" ")
    print(f'[认证检查] Scheme: {scheme}, Token 长度: {len(token) if token else 0}')
    
    if scheme.lower() != "bearer":
        print(f'[认证失败] 无效的认证方案: {scheme}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_access_token(token)
        if payload is None:
            print('[认证失败] Token 解码返回 None')
            raise credentials_exception
        user_id: int = payload.get("sub")
        print(f'[认证成功] 解析出用户ID: {user_id}')
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        print(f'[认证失败] JWT 错误: {str(e)}')
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        print(f'[认证失败] 数据库中未找到用户ID: {user_id}')
        raise credentials_exception
    print(f'[认证成功] 用户: {user.account}\n')
    return user

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.account == user.account).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Account already registered")
    
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        account=user.account,
        password_hash=hashed_password,
        nickname=user.nickname,
        real_name=user.real_name,
        student_id=user.student_id,
        major=user.major
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.account == user.account).first()
    if not db_user or not security.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect account or password")
    
    access_token_expires = security.timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.UserResponse)
def update_user_me(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f'更新用户资料 - 用户ID: {current_user.id}')
    print(f'接收到的数据: {user_update.model_dump(exclude_unset=True)}')
    
    try:
        # 验证 bio 长度
        if user_update.bio is not None and len(user_update.bio) > 150:
            raise HTTPException(status_code=400, detail="个性签名不能超过150字")
        
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(current_user, field, value)
        db.commit()
        db.refresh(current_user)
        print(f'用户资料更新成功')
        return current_user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f'更新用户资料失败: {str(e)}')
        raise HTTPException(status_code=500, detail=f"更新失败: {str(e)}")

@router.post("/avatar", response_model=dict)
def upload_avatar(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user)
):
    """
    上传用户头像
    支持格式: jpg, png, webp
    最大大小: 2MB
    """
    print(f'\n=== 头像上传请求 ===')
    print(f'用户ID: {current_user.id}')
    print(f'用户名: {current_user.account}')
    print(f'文件名: {file.filename}')
    print(f'文件类型: {file.content_type}')
    print(f'=====================\n')
    
    try:
        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/png', 'image/webp']
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型: {file.content_type}。仅支持 JPG、PNG、WEBP 格式"
            )
        
        # 读取文件内容并检查大小
        contents = file.file.read()
        file_size = len(contents)
        max_size = 2 * 1024 * 1024  # 2MB
        
        if file_size > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"文件大小超过限制 ({file_size / 1024 / 1024:.2f}MB > 2MB)"
            )
        
        print(f'文件大小: {file_size / 1024:.2f}KB')
        
        # 生成唯一文件名
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # 确保上传目录存在
        upload_dir = Path("uploads/avatars")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存文件
        file_path = upload_dir / unique_filename
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # 生成访问 URL
        avatar_url = f"/uploads/avatars/{unique_filename}"
        
        print(f'头像上传成功: {avatar_url}')
        
        return {
            "message": "头像上传成功",
            "avatar_url": avatar_url
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f'头像上传失败: {str(e)}')
        raise HTTPException(
            status_code=500,
            detail=f"上传失败: {str(e)}"
        )
