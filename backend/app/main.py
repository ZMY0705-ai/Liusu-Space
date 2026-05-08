from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.database import engine, Base
from app.routers import users, works, interactions, forum, notifications

# 创建数据库表（如果不存在）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="流俗地 API", version="1.0.0")

# 配置静态文件服务
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应限制为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(users.router)
app.include_router(works.router)
app.include_router(interactions.router)
app.include_router(forum.router)
app.include_router(notifications.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Liusu Space API"}
