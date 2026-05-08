from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- User Schemas ---
class UserRegister(BaseModel):
    account: str
    password: str
    nickname: str
    real_name: Optional[str] = None
    student_id: Optional[str] = None
    major: Optional[str] = None

class UserLogin(BaseModel):
    account: str
    password: str

class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    signature: Optional[str] = None
    real_name: Optional[str] = None
    student_id: Optional[str] = None
    major: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    account: str
    nickname: str
    avatar: Optional[str] = None
    signature: Optional[str] = None
    real_name: Optional[str] = None
    student_id: Optional[str] = None
    major: Optional[str] = None

    class Config:
        from_attributes = True

# --- Work Schemas ---
class WorkCreate(BaseModel):
    title: str
    content: str
    cover_image: Optional[str] = None
    status: int = 0 # 0=draft, 1=published
    is_published: bool = False # True=发表作品（首页可见），False=保存作品（仅我的作品可见）

class WorkUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    cover_image: Optional[str] = None
    status: Optional[int] = None
    is_published: Optional[bool] = None  # True=发表作品（首页可见），False=保存作品（仅我的作品可见）

class WorkCommentCreate(BaseModel):
    content: str

class WorkResponse(BaseModel):
    id: int
    author_id: int
    title: str
    content: str
    cover_image: Optional[str] = None
    status: int
    view_count: int
    like_count: int
    comment_count: int
    favorite_count: int
    created_at: datetime
    published_at: Optional[datetime] = None
    author: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# --- Forum Schemas ---
class PostCreate(BaseModel):
    title: str
    content: str

class PostCommentCreate(BaseModel):
    content: str
    parent_id: Optional[int] = None

class PostResponse(BaseModel):
    id: int
    author_id: int
    title: str
    content: str
    comment_count: int
    created_at: datetime
    author: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# --- Notification Schemas ---
class NotificationResponse(BaseModel):
    id: int
    type: str
    sender_id: int
    target_type: str
    target_id: int
    content: Optional[str] = None
    is_read: bool
    created_at: datetime
    sender: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# --- Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str
