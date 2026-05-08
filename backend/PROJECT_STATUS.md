# 流俗地 (Liusu Space) - 项目状态摘要

> **最后更新**: 2026-04-23  
> **版本**: v1.0.0  
> **状态**: ✅ 后端开发完成，所有接口测试通过

---

## 📋 目录

1. [项目概述](#项目概述)
2. [技术栈](#技术栈)
3. [环境配置](#环境配置)
4. [数据库架构](#数据库架构)
5. [API 接口文档](#api-接口文档)
6. [项目结构](#项目结构)
7. [关键依赖版本](#关键依赖版本)
8. [启动指南](#启动指南)
9. [已知问题与注意事项](#已知问题与注意事项)

---

## 项目概述

**流俗地**是一个校园文学社区 APP 的后端服务，提供用户管理、作品发布、互动评论、论坛交流、消息通知等核心功能。

### 核心功能模块
- 👤 **用户系统**: 注册、登录、JWT 认证、个人信息管理
- 📚 **作品管理**: 创作、发布、编辑、删除文学作品
- 💬 **互动功能**: 点赞、收藏、评论作品
- 📝 **论坛社区**: 发帖、回复、楼中楼评论
- 🔔 **消息通知**: 点赞、评论、收藏、回复通知

---

## 技术栈

### 后端框架
- **FastAPI** 0.109.0 - 现代 Web 框架
- **SQLAlchemy** 2.0.25 - ORM 数据库映射
- **Pydantic** 2.5.3 - 数据验证
- **Uvicorn** 0.46.0 - ASGI 服务器

### 数据库
- **MySQL 8.0+** - 关系型数据库
- **PyMySQL** 1.1.2 - MySQL 驱动

### 认证与安全
- **python-jose** 3.5.0 - JWT Token 生成与验证
- **passlib** 1.7.4 - 密码哈希
- **bcrypt** 4.0.1 - 加密算法

### 其他工具
- **python-dotenv** 1.2.2 - 环境变量管理
- **python-multipart** 0.0.26 - 文件上传支持

---

## 环境配置

### 系统要求
- **Python**: 3.14.4 (或 3.11+)
- **MySQL**: 8.0+
- **操作系统**: Windows 10/11, Linux, macOS

### 环境变量 (.env)

```env
# 数据库连接
DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/liususpace?charset=utf8mb4

# JWT 配置
SECRET_KEY=your-super-secret-key-for-jwt-signing
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 数据库配置
- **数据库名**: `liususpace`
- **字符集**: `utf8mb4`
- **排序规则**: `utf8mb4_unicode_ci`
- **引擎**: InnoDB

---

## 数据库架构

### 表结构概览（8 张表）

| 表名 | 说明 | 主要字段 |
|------|------|---------|
| `users` | 用户表 | id, account, password_hash, nickname, avatar, signature |
| `works` | 作品表 | id, author_id, title, content, status, view_count |
| `work_comments` | 作品评论表 | id, work_id, user_id, content |
| `work_likes` | 作品点赞表 | work_id, user_id (联合主键) |
| `work_favorites` | 作品收藏表 | work_id, user_id (联合主键) |
| `forum_posts` | 论坛帖子表 | id, author_id, title, content, comment_count |
| `post_comments` | 帖子回复表 | id, post_id, user_id, content, parent_id |
| `notifications` | 消息通知表 | id, user_id, type, sender_id, target_type, is_read |

### 关键字段类型映射

| MySQL 类型 | SQLAlchemy 类型 | 说明 |
|-----------|----------------|------|
| `BIGINT UNSIGNED` | `BIGINT(unsigned=True)` | 所有主键和外键 |
| `TINYINT` | `SmallInteger` | status, role, is_read 等状态字段 |
| `VARCHAR(n)` | `String(n)` | 字符串字段 |
| `TEXT` | `Text` | 长文本内容 |
| `DATETIME` | `DateTime` | 时间戳字段 |

---

## API 接口文档

### 基础信息
- **后端 URL**: `http://127.0.0.1:8000`
- **前端 URL**: `http://localhost:3002`
- **API 文档**: http://127.0.0.1:8000/docs (Swagger UI)
- **认证方式**: Bearer Token (JWT)
- **数据格式**: JSON

### 1. 用户模块 (`/users`)

| 方法 | 路径 | 说明 | 认证 | 请求体 |
|------|------|------|------|--------|
| POST | `/users/register` | 用户注册 | ❌ | `UserRegister` |
| POST | `/users/login` | 用户登录 | ❌ | `UserLogin` |
| GET | `/users/me` | 获取当前用户信息 | ✅ | - |
| PUT | `/users/me` | 更新当前用户信息 | ✅ | `UserUpdate` |

**请求体示例 - 注册**:
```json
{
  "account": "testuser",
  "password": "test123",
  "nickname": "测试用户",
  "real_name": "张三",
  "student_id": "20240001",
  "major": "计算机科学与技术"
}
```

### 2. 作品模块 (`/works`)

| 方法 | 路径 | 说明 | 认证 | 请求体 |
|------|------|------|------|--------|
| POST | `/works/` | 创建作品 | ✅ | `WorkCreate` |
| GET | `/works/` | 获取已发布作品列表 | ❌ | 查询参数: skip, limit |
| GET | `/works/{work_id}` | 获取作品详情 | ❌ | - |
| PUT | `/works/{work_id}` | 更新作品 | ✅ | `WorkUpdate` |
| DELETE | `/works/{work_id}` | 删除作品 | ✅ | - |
| POST | `/works/upload-cover` | 上传封面图片 | ❌ | FormData (file) |

**请求体示例 - 创建作品**:
```json
{
  "title": "我的第一篇小说",
  "content": "这是小说的内容...",
  "cover_image": null,
  "status": 1
}
```

### 3. 互动模块 (`/interactions`)

| 方法 | 路径 | 说明 | 认证 | 请求体 |
|------|------|------|------|--------|
| POST | `/works/{work_id}/comments` | 评论作品 | ✅ | `WorkCommentCreate` |
| GET | `/works/{work_id}/comments` | 获取作品评论列表 | ❌ | - |
| POST | `/works/{work_id}/like` | 点赞/取消点赞 | ✅ | - |
| POST | `/works/{work_id}/favorite` | 收藏/取消收藏 | ✅ | - |

**请求体示例 - 评论**:
```json
{
  "content": "写得太好了！"
}
```

### 4. 论坛模块 (`/forum`)

| 方法 | 路径 | 说明 | 认证 | 请求体 |
|------|------|------|------|--------|
| POST | `/forum/posts` | 创建帖子 | ✅ | `PostCreate` |
| GET | `/forum/posts` | 获取帖子列表 | ❌ | 查询参数: skip, limit |
| GET | `/forum/posts/{post_id}` | 获取帖子详情 | ❌ | - |
| POST | `/forum/posts/{post_id}/comments` | 回复帖子 | ✅ | `PostCommentCreate` |
| GET | `/forum/posts/{post_id}/comments` | 获取帖子回复列表 | ❌ | - |

**请求体示例 - 创建帖子**:
```json
{
  "title": "讨论：如何写好一篇散文",
  "content": "大家好，今天想和大家聊聊..."
}
```

### 5. 通知模块 (`/notifications`)

| 方法 | 路径 | 说明 | 认证 | 请求体 |
|------|------|------|------|--------|
| GET | `/notifications/` | 获取我的通知列表 | ✅ | - |
| PUT | `/notifications/{notification_id}/read` | 标记通知为已读 | ✅ | - |
| PUT | `/notifications/read-all` | 全部标记为已读 | ✅ | - |

### 认证机制

**获取 Token**:
```http
POST /users/login
Content-Type: application/json

{
  "account": "testuser",
  "password": "test123"
}
```

**响应**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**使用 Token**:
```http
GET /users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── database.py          # 数据库配置
│   ├── models.py            # SQLAlchemy 模型定义
│   ├── schemas.py           # Pydantic 数据验证模型
│   ├── security.py          # JWT 和密码加密
│   └── routers/
│       ├── users.py         # 用户相关接口
│       ├── works.py         # 作品相关接口
│       ├── interactions.py  # 互动功能接口
│       ├── forum.py         # 论坛功能接口
│       └── notifications.py # 通知功能接口
├── uploads/                 # 上传文件存储目录
│   └── covers/             # 作品封面图片
├── .env                     # 环境变量配置
├── requirements.txt         # Python 依赖列表
├── test_api.py              # 单接口测试脚本
└── test_all_apis.py         # 全量接口测试脚本
```

---

## 关键依赖版本

| 依赖包 | 版本 | 说明 | 注意事项 |
|--------|------|------|---------|
| fastapi | 0.109.0 | Web 框架 | 与 Pydantic 2.5.3 兼容 |
| uvicorn | 0.46.0 | ASGI 服务器 | 实际安装版本可能高于 requirements.txt |
| sqlalchemy | 2.0.49 | ORM | 需要使用 BIGINT(unsigned=True) |
| pymysql | 1.1.2 | MySQL 驱动 | - |
| pydantic | 2.13.3 | 数据验证 | 使用 model_dump() 而非 dict() |
| python-jose | 3.5.0 | JWT | - |
| passlib | 1.7.4 | 密码哈希 | - |
| bcrypt | 4.0.1 | 加密算法 | ⚠️ 不能使用 5.x 版本 |
| python-dotenv | 1.2.2 | 环境变量 | - |
| python-multipart | 0.0.26 | 文件上传 | - |

---

## 启动指南

### 1. 环境准备

```powershell
# 检查 Python 版本
py --version  # 应该显示 Python 3.14.4 或更高

# 检查 MySQL 服务
Get-Service | Where-Object {$_.Name -like "*mysql*"}
```

### 2. 安装依赖

```powershell
# 进入项目目录
cd d:\HuaweiMoveData\Users\33294\Desktop\流俗地\backend

# 安装依赖
py -m pip install -r requirements.txt

# 确保 bcrypt 版本正确
py -m pip install bcrypt==4.0.1
```

### 3. 配置数据库

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS liususpace
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 执行建表 SQL（参考项目根目录的建表语句）
USE liususpace;
-- ... 执行 8 张表的 CREATE TABLE 语句
```

### 4. 启动服务

```powershell
# 启动后端开发服务器
cd d:\HuaweiMoveData\Users\33294\Desktop\流俗地\backend
py -m uvicorn app.main:app --reload

# 后端服务将在 http://127.0.0.1:8000 启动

# 启动前端开发服务器（新终端）
cd d:\HuaweiMoveData\Users\33294\Desktop\流俗地\frontend
npm run dev

# 前端服务将在 http://localhost:3002 启动
```

### 5. 验证服务

```powershell
# 运行全量测试
py test_all_apis.py

# 或者访问 API 文档
# 浏览器打开: http://127.0.0.1:8000/docs

# 访问前端
# 浏览器打开: http://localhost:3002
```

---

## 已知问题与注意事项

### ⚠️ 重要警告

1. **bcrypt 版本锁定**
   - ❌ 不要升级到 bcrypt 5.x，会导致 passlib 不兼容
   - ✅ 始终使用 `bcrypt==4.0.1`
   - 📝 在 `requirements.txt` 中已添加注释说明

2. **Pydantic v2 API 变更**
   - ✅ 使用 `.model_dump()` 替代 `.dict()`
   - ✅ 使用 `.model_validate()` 替代 `.parse_obj()`

3. **MySQL 类型映射**
   - ✅ 所有 `BIGINT UNSIGNED` 使用 `BIGINT(unsigned=True)`
   - ✅ 所有 `TINYINT` 使用 `SmallInteger`，不用 `Boolean`
   - ✅ `is_read` 字段使用 0/1 而非 True/False

4. **生产环境配置**
   - ⚠️ `.env` 中的 `SECRET_KEY` 必须更换为强随机密钥
   - ⚠️ CORS 配置 `allow_origins=["*"]` 应限制为前端域名
   - ⚠️ 数据库密码应从环境变量读取，不要硬编码

### 🔧 常见问题排查

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| 500 错误 | bcrypt 版本不兼容 | 降级到 4.0.1 |
| 422 错误 | Pydantic 验证失败 | 检查请求体格式 |
| 数据库连接失败 | MySQL 未启动或密码错误 | 检查服务和 .env 配置 |
| ModuleNotFoundError | 未在 backend 目录运行 | `cd backend` 后再启动 |
| 文件上传失败 | uploads 目录权限问题 | 确保目录存在且可写 |

### 📞 测试账号

系统已创建测试账号：
- **账号**: `testuser001` / **密码**: `123456` (ID: 1)
- **账号**: `testuser002` / **密码**: `123456` (ID: 2)

---

## 更新日志

### v1.0.0 (2026-04-23)
- ✅ 完成所有核心功能模块开发
- ✅ 修复 bcrypt 兼容性问题
- ✅ 修复 SQLAlchemy 类型映射问题
- ✅ 修复 Pydantic v2 API 兼容性问题
- ✅ 通过全量接口测试（10/10 通过）

---

## 联系方式

如有问题，请参考：
- 后端 API 文档: http://127.0.0.1:8000/docs
- 前端应用: http://localhost:3002
- 项目根目录: `d:\HuaweiMoveData\Users\33294\Desktop\流俗地`

---

**文档生成时间**: 2026-04-23  
**维护者**: 流俗地开发团队
