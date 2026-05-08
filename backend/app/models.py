from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, SmallInteger
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(BIGINT(unsigned=True), primary_key=True, index=True)
    account = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nickname = Column(String(30), nullable=False)
    avatar = Column(String(500))
    signature = Column(String(100))
    real_name = Column(String(20))
    student_id = Column(String(20))
    major = Column(String(50))
    role = Column(SmallInteger, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    works = relationship("Work", back_populates="author")
    comments = relationship("WorkComment", back_populates="user")
    forum_posts = relationship("ForumPost", back_populates="author")
    post_comments = relationship("PostComment", back_populates="user")
    notifications_received = relationship("Notification", foreign_keys="[Notification.user_id]", back_populates="user")
    notifications_sent = relationship("Notification", foreign_keys="[Notification.sender_id]", back_populates="sender")

class Work(Base):
    __tablename__ = "works"

    id = Column(BIGINT(unsigned=True), primary_key=True, index=True)
    author_id = Column(BIGINT(unsigned=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(60), nullable=False)
    content = Column(Text, nullable=False)
    cover_image = Column(String(500))
    status = Column(SmallInteger, default=0) # 0=draft, 1=published
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    published_at = Column(DateTime)

    author = relationship("User", back_populates="works")
    comments = relationship("WorkComment", back_populates="work")
    likes = relationship("WorkLike", back_populates="work")
    favorites = relationship("WorkFavorite", back_populates="work")

class WorkComment(Base):
    __tablename__ = "work_comments"

    id = Column(BIGINT(unsigned=True), primary_key=True, index=True)
    work_id = Column(BIGINT(unsigned=True), ForeignKey("works.id"), nullable=False)
    user_id = Column(BIGINT(unsigned=True), ForeignKey("users.id"), nullable=False)
    content = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    work = relationship("Work", back_populates="comments")
    user = relationship("User", back_populates="comments")

class WorkLike(Base):
    __tablename__ = "work_likes"

    work_id = Column(BIGINT(unsigned=True), ForeignKey("works.id"), primary_key=True)
    user_id = Column(BIGINT(unsigned=True), ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())

    work = relationship("Work", back_populates="likes")
    user = relationship("User")

class WorkFavorite(Base):
    __tablename__ = "work_favorites"

    work_id = Column(BIGINT(unsigned=True), ForeignKey("works.id"), primary_key=True)
    user_id = Column(BIGINT(unsigned=True), ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())

    work = relationship("Work", back_populates="favorites")
    user = relationship("User")

class ForumPost(Base):
    __tablename__ = "forum_posts"

    id = Column(BIGINT(unsigned=True), primary_key=True, index=True)
    author_id = Column(BIGINT(unsigned=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    comment_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    author = relationship("User", back_populates="forum_posts")
    comments = relationship("PostComment", back_populates="post")

class PostComment(Base):
    __tablename__ = "post_comments"

    id = Column(BIGINT(unsigned=True), primary_key=True, index=True)
    post_id = Column(BIGINT(unsigned=True), ForeignKey("forum_posts.id"), nullable=False)
    user_id = Column(BIGINT(unsigned=True), ForeignKey("users.id"), nullable=False)
    content = Column(String(500), nullable=False)
    parent_id = Column(BIGINT(unsigned=True), ForeignKey("post_comments.id"))
    created_at = Column(DateTime, server_default=func.now())

    post = relationship("ForumPost", back_populates="comments")
    user = relationship("User", back_populates="post_comments")
    parent = relationship("PostComment", remote_side=[id])

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(BIGINT(unsigned=True), primary_key=True, index=True)
    user_id = Column(BIGINT(unsigned=True), ForeignKey("users.id"), nullable=False)
    type = Column(String(20), nullable=False) # like, comment, favorite, reply
    sender_id = Column(BIGINT(unsigned=True), ForeignKey("users.id"), nullable=False)
    target_type = Column(String(20), nullable=False) # work, post
    target_id = Column(BIGINT(unsigned=True), nullable=False)
    content = Column(String(200))
    is_read = Column(SmallInteger, default=0) # 0=未读,1=已读
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", foreign_keys=[user_id], back_populates="notifications_received")
    sender = relationship("User", foreign_keys=[sender_id], back_populates="notifications_sent")
