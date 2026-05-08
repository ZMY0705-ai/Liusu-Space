# MeCenter 个人资料显示修复说明

## 🔧 已修复的问题

### 问题描述
用户在"编辑资料"页面修改了头像、个性签名、真实姓名/专业等信息并保存后，返回"我的"页面（MeCenter.vue）时，**新数据没有显示出来**。

### 根本原因
1. **MeCenter.vue 只使用了 `authStore.user`**，但这个数据在编辑后没有自动刷新
2. **缺少 `onActivated` 钩子**，从编辑页面返回时不会重新获取用户信息
3. **模板中缺少新字段的渲染**：bio、real_name、major、is_real_name_public、is_major_public
4. **头像显示逻辑不完整**：只支持首字母占位符，不支持图片 URL

---

## ✅ 修复内容

### 1. MeCenter.vue 模板增强

#### 头像显示（支持图片 + 占位符）
```vue
<div class="user-avatar">
  <img 
    v-if="authStore.user?.avatar" 
    :src="getFullAvatarUrl(authStore.user.avatar)" 
    alt="头像"
    class="avatar-img"
  />
  <span v-else>{{ getAuthorInitial(authStore.user?.nickname || 'U') }}</span>
</div>
```

#### 个性签名（优先显示 bio，兼容旧字段 signature）
```vue
<!-- 个性签名 -->
<p v-if="authStore.user?.bio" class="user-signature">{{ authStore.user.bio }}</p>
<p v-else-if="authStore.user?.signature" class="user-signature">{{ authStore.user.signature }}</p>
```

#### 公开的真实姓名（带隐私控制）
```vue
<!-- 公开的真实姓名 -->
<p v-if="authStore.user?.is_real_name_public && authStore.user?.real_name" class="user-real-name">
  📝 {{ authStore.user.real_name }}
</p>
```

#### 公开的专业（带隐私控制）
```vue
<!-- 公开的专业 -->
<p v-if="authStore.user?.is_major_public && authStore.user?.major" class="user-major">
  🎓 {{ authStore.user.major }}
</p>
```

### 2. 新增工具函数

```typescript
// 获取完整头像URL（处理相对路径）
const getFullAvatarUrl = (url: string | undefined) => {
  if (!url) return ''
  // 如果是相对路径，拼接后端地址
  if (url.startsWith('/')) {
    return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}${url}`
  }
  return url
}
```

### 3. 添加 onActivated 钩子（关键修复）

```typescript
import { ref, onMounted, onActivated } from 'vue'

// ... 其他代码 ...

// 当页面被激活时（从其他页面返回），重新获取用户信息
onActivated(async () => {
  console.log('[MeCenter] 页面被激活，刷新用户信息')
  await authStore.fetchUser()
})
```

**作用**：
- 当用户从"编辑资料"页面返回"我的"页面时
- `onActivated` 会自动触发
- 调用 `authStore.fetchUser()` 从后端重新获取最新的用户信息
- 确保页面上显示的是最新数据

### 4. CSS 样式增强

```css
.user-real-name,
.user-major {
  font-size: 13px;
  opacity: 0.85;
  margin: 4px 0 0 0;
}

.avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}
```

---

## 🧪 测试步骤

### 1. 重启前端服务（如果未重启）
```bash
cd d:\HuaweiMoveData\Users\33294\Desktop\流俗地\frontend
npm run dev
```

### 2. 打开浏览器控制台
访问 http://localhost:3002，按 F12 打开开发者工具

### 3. 测试流程

#### 步骤 A：编辑资料
1. 登录账号
2. 点击底部导航栏的 **"我的"**
3. 点击右上角的 **"编辑"** 按钮
4. 修改以下字段：
   - 📸 上传新头像
   - ✏️ 修改昵称
   - 📝 填写个性签名（bio）
   - 📛 填写真实姓名
   - 🎓 填写专业/学院
   - 🔒 开启"公开真实姓名"开关
   - 🔒 开启"公开专业"开关
5. 点击 **"保存"** 按钮
6. 等待 Toast 提示"保存成功"

#### 步骤 B：验证数据显示
1. 自动返回"我的"页面后，观察：
   - ✅ 头像是否更新为新上传的图片
   - ✅ 昵称是否更新
   - ✅ 个性签名是否显示
   - ✅ 是否显示"📝 真实姓名"
   - ✅ 是否显示"🎓 专业/学院"

2. 查看浏览器控制台，应该看到：
   ```
   [MeCenter] 页面被激活，刷新用户信息
   ```

3. 查看 Network 标签：
   - 找到 `GET /users/me` 请求
   - 查看 Response，确认包含：
     ```json
     {
       "id": 1,
       "account": "testuser",
       "nickname": "新昵称",
       "avatar": "/uploads/avatars/xxx.jpg",
       "bio": "新的个性签名",
       "real_name": "张三",
       "major": "计算机科学",
       "is_real_name_public": true,
       "is_major_public": true
     }
     ```

### 4. 测试隐私开关

#### 测试关闭公开
1. 再次进入"编辑资料"
2. 关闭"公开真实姓名"开关
3. 关闭"公开专业"开关
4. 保存并返回
5. 验证：
   - ❌ "📝 真实姓名" 应该消失
   - ❌ "🎓 专业/学院" 应该消失

#### 测试部分公开
1. 只开启"公开真实姓名"
2. 保存并返回
3. 验证：
   - ✅ 只显示"📝 真实姓名"
   - ❌ 不显示"🎓 专业/学院"

---

## 🔍 常见问题排查

### Q1: 头像上传成功但不显示？
**检查清单**：
1. 打开浏览器控制台 → Network 标签
2. 找到头像图片的请求（类似 `/uploads/avatars/xxx.jpg`）
3. 查看状态码：
   - **200**：图片加载成功，检查 CSS 样式
   - **404**：图片路径错误，检查 `getFullAvatarUrl` 函数
   - **403**：权限问题，检查后端静态文件配置

**解决方案**：
确保后端 `main.py` 中配置了静态文件服务：
```python
from fastapi.staticfiles import StaticFiles

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
```

### Q2: 返回"我的"页面后数据没刷新？
**检查清单**：
1. 打开浏览器控制台
2. 查看是否有 `[MeCenter] 页面被激活，刷新用户信息` 日志
3. 如果没有，检查路由配置是否正确

**解决方案**：
确保路由配置中使用了 `keep-alive`：
```typescript
// router/index.ts
{
  path: '/me',
  component: () => import('@/ui/pages/MeCenter.vue'),
  meta: { keepAlive: true }  // 启用缓存
}
```

并在 App.vue 中使用：
```vue
<router-view v-slot="{ Component }">
  <keep-alive>
    <component :is="Component" v-if="$route.meta.keepAlive" />
  </keep-alive>
  <component :is="Component" v-if="!$route.meta.keepAlive" />
</router-view>
```

### Q3: bio 和 signature 都显示了？
**检查清单**：
1. 确认模板中使用了 `v-if` 和 `v-else-if`
2. 不应该同时显示两个字段

**当前实现**（正确）：
```vue
<p v-if="authStore.user?.bio" class="user-signature">{{ authStore.user.bio }}</p>
<p v-else-if="authStore.user?.signature" class="user-signature">{{ authStore.user.signature }}</p>
```

### Q4: 后端返回的数据里没有新字段？
**检查清单**：
1. 打开浏览器控制台 → Network 标签
2. 找到 `GET /users/me` 请求
3. 查看 Response 是否包含：
   - `bio`
   - `is_real_name_public`
   - `is_major_public`

**如果没有这些字段**：
- 检查数据库是否已添加这些字段（执行 ALTER TABLE）
- 检查后端 `models.py` 是否定义了这些字段
- 检查后端 `schemas.py` 的 `UserResponse` 是否包含这些字段
- 重启后端服务

---

## 📊 预期效果对比

### 修复前
```
┌─────────────────────┐
│  [U]  用户名         │  ← 只有首字母占位符
│  user@example.com   │
│                     │  ← 没有个性签名
│                     │  ← 没有真实姓名
│                     │  ← 没有专业信息
└─────────────────────┘
```

### 修复后
```
┌─────────────────────┐
│  [📸]  新昵称        │  ← 显示上传的头像
│  user@example.com   │
│  用一句话定义自己... │  ← 显示个性签名
│  📝 张三            │  ← 显示真实姓名（如果公开）
│  🎓 计算机科学       │  ← 显示专业（如果公开）
└─────────────────────┘
```

---

## 🎯 技术要点总结

### 1. Vue 3 生命周期钩子
- **`onMounted`**：组件首次挂载时执行
- **`onActivated`**：keep-alive 缓存的组件被激活时执行（从其他页面返回）

### 2. Pinia Store 响应式更新
- `authStore.user` 是响应式的
- 调用 `authStore.fetchUser()` 会更新 store
- 所有使用 `authStore.user` 的组件会自动重新渲染

### 3. 条件渲染最佳实践
```vue
<!-- ✅ 正确：使用 v-if / v-else-if -->
<p v-if="user?.bio">{{ user.bio }}</p>
<p v-else-if="user?.signature">{{ user.signature }}</p>

<!-- ❌ 错误：两个都会显示 -->
<p v-if="user?.bio">{{ user.bio }}</p>
<p v-if="user?.signature">{{ user.signature }}</p>
```

### 4. 隐私控制的实现
```vue
<!-- 只有 is_real_name_public 为 true 且 real_name 有值时才显示 -->
<p v-if="user?.is_real_name_public && user?.real_name">
  📝 {{ user.real_name }}
</p>
```

---

## ✅ 验证成功的标志

如果看到以下现象，说明修复成功：

1. ✅ 上传头像后立即在"我的"页面显示新头像
2. ✅ 修改昵称后，"我的"页面立即显示新昵称
3. ✅ 填写个性签名后，"我的"页面立即显示
4. ✅ 开启"公开真实姓名"后，显示"📝 真实姓名"
5. ✅ 开启"公开专业"后，显示"🎓 专业/学院"
6. ✅ 关闭公开开关后，对应信息立即隐藏
7. ✅ 浏览器控制台显示 `[MeCenter] 页面被激活，刷新用户信息`
8. ✅ Network 标签中 `GET /users/me` 返回完整的新字段

---

**修复完成时间**: 2026-05-08  
**修复人员**: AI Assistant  
**相关 Issue**: MeCenter 个人资料显示缺失
