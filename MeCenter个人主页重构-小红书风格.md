# MeCenter 个人主页重构 - 小红书风格

## 🎨 重构概述

将"我的"页面顶部个人资料区域从简陋的垂直列表重构为**小红书风格的个人主页**布局，采用"背景封面 + 头像浮层"的设计。

---

## ✨ 新设计特点

### 1. 背景封面
- ✅ 140px 高度的渐变背景图
- ✅ 抹茶绿 → 浅绿 → 柠檬黄三色渐变
- ✅ 叠加半透明圆形光晕效果
- ✅ 治愈系自然风格

### 2. 头像浮层效果
- ✅ 90px 大圆形头像
- ✅ 白色边框 + 柔和阴影
- ✅ 一半在背景图上，一半在白色区域（margin-top: -45px）
- ✅ 如果没有头像，显示首字母占位符

### 3. 用户信息布局
- ✅ **删除账号名显示**（只显示昵称，不显示 account）
- ✅ 昵称右侧对齐，20px 粗体字
- ✅ 专业标签采用胶囊样式（灰色圆角背景）
- ✅ 个性签名最多显示 2 行，超出省略

### 4. 编辑资料按钮
- ✅ 圆角浅灰色边框样式
- ✅ 右上角对齐
- ✅ 点击态背景变浅灰

### 5. 数据统计栏
- ✅ 横向排列三个统计数字：作品、草稿、收藏
- ✅ 数字 18px 粗体，标签 12px 灰色
- ✅ 点击时有缩放动画
- ✅ 顶部有分割线

---

## 📊 效果对比

### 重构前
```
┌──────────────────────────────┐
│  [渐变绿色背景]               │
│  [U]  用户名                  │  ← 首字母占位符
│  user@example.com            │  ← 显示账号名
│  个性签名                     │
│  📝 张三                      │
│  🎓 计算机科学                │
│              [编辑]           │
└──────────────────────────────┘
```

### 重构后
```
┌──────────────────────────────┐
│  [渐变背景 + 光晕效果]        │  ← 140px 高度
│                              │
│      [头像]                  │  ← 浮层效果
│        昵称                   │
│        [计算机科学]           │  ← 胶囊标签
│        个性签名...            │
│              [编辑资料]       │
├──────────────────────────────┤
│  12       5        8         │  ← 数据统计
│  作品     草稿     收藏       │
└──────────────────────────────┘
```

---

##  技术实现

### HTML 结构
```vue
<div class="profile-header">
  <!-- 背景封面 -->
  <div class="cover-banner">
    <div class="cover-gradient"></div>
  </div>

  <!-- 头像和信息区域 -->
  <div class="profile-info-section">
    <div class="avatar-wrapper">
      <div class="user-avatar">
        <img v-if="avatar" :src="avatar" />
        <span v-else>{{ initial }}</span>
      </div>
    </div>

    <div class="user-details">
      <h2 class="nickname">{{ nickname }}</h2>
      <div class="tags-row">
        <span class="tag-pill">{{ major }}</span>
      </div>
      <p class="bio-text">{{ bio }}</p>
    </div>

    <van-button class="edit-profile-btn">编辑资料</van-button>
  </div>

  <!-- 数据统计栏 -->
  <div class="stats-bar">
    <div class="stat-item">
      <span class="stat-number">{{ works.length }}</span>
      <span class="stat-label">作品</span>
    </div>
    ...
  </div>
</div>
```

### CSS 关键样式

#### 1. 背景封面渐变
```css
.cover-gradient {
  background: linear-gradient(135deg, #64A386 0%, #A8D5A1 50%, #F5B342 100%);
}

.cover-gradient::before {
  background: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.2) 0%, transparent 40%);
}
```

#### 2. 头像浮层效果
```css
.profile-info-section {
  margin-top: -45px; /* 让头像向上浮出 45px */
}

.user-avatar {
  width: 90px;
  height: 90px;
  border: 4px solid var(--pure-white); /* 白色边框 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); /* 柔和阴影 */
}
```

#### 3. 胶囊标签
```css
.tag-pill {
  padding: 4px 12px;
  background: #F5F5F5;
  border-radius: 12px; /* 圆角胶囊 */
  font-size: 12px;
}
```

#### 4. 数据统计
```css
.stat-number {
  font-size: 18px;
  font-weight: 700;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
}
```

---

## 🎯 关键改进点

### 1. 删除账号名显示
**修改前**：
```vue
<p class="user-detail">{{ authStore.user?.account || '' }}</p>
```

**修改后**：
```vue
<!-- 完全移除 account 显示 -->
<h2 class="nickname">{{ authStore.user?.nickname || '未登录' }}</h2>
```

### 2. 专业标签改为胶囊样式
**修改前**：
```vue
<p class="user-major">🎓 {{ authStore.user.major }}</p>
```

**修改后**：
```vue
<div class="tags-row">
  <span class="tag-pill">{{ authStore.user.major }}</span>
</div>
```

### 3. 真实姓名不再显示
**修改前**：
```vue
<p v-if="authStore.user?.is_real_name_public && authStore.user?.real_name">
   {{ authStore.user.real_name }}
</p>
```

**修改后**：
```vue
<!-- 完全移除真实姓名显示 -->
```

### 4. 数据统计栏
**新增功能**：
```vue
<div class="stats-bar">
  <div class="stat-item">
    <span class="stat-number">{{ myWorks.length }}</span>
    <span class="stat-label">作品</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">{{ myDrafts.length }}</span>
    <span class="stat-label">草稿</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">{{ myFavorites.length }}</span>
    <span class="stat-label">收藏</span>
  </div>
</div>
```

---

## 🎨 视觉规范

### 颜色使用
- **背景渐变**：抹茶绿 (#64A386) → 浅绿 (#A8D5A1) → 柠檬黄 (#F5B342)
- **头像边框**：纯白色 (#FFFFFF)
- **昵称文字**：墨黑色 (var(--ink-dark))
- **签名文字**：浅灰色 (var(--text-secondary))
- **标签背景**：极浅灰 (#F5F5F5)
- **按钮边框**：浅灰 (#E0E0E0)
- **分割线**：极浅灰 (#F0F0F0)

### 圆角规范
- **头像**：50%（完美圆形）
- **标签胶囊**：12px
- **编辑按钮**：16px
- **作品卡片**：16px

### 阴影规范
- **头像阴影**：`0 4px 12px rgba(0, 0, 0, 0.08)`
- **按钮按压**：背景变 #F5F5F5

### 字号规范
- **昵称**：20px，700 粗体
- **统计数字**：18px，700 粗体
- **个性签名**：14px，400 常规
- **标签文字**：12px，500 中等
- **统计标签**：12px，400 常规

---

## 📝 代码修改清单

### 修改的文件
1. ✅ `frontend/src/ui/pages/MeCenter.vue`
   - 模板部分：完全重构头部结构
   - 样式部分：新增 153 行样式，删除 84 行旧样式

### 删除的代码
- ❌ `.user-card` 样式（绿色背景卡片）
- ❌ `.leaf-decoration` SVG 装饰
- ❌ `.user-detail` 账号名显示
- ❌ `.user-real-name` 真实姓名显示
- ❌ `.user-major` 专业显示（改为标签）
- ❌ `.edit-btn` 旧编辑按钮
- ❌ `.btn-login` 登录按钮（未登录状态改用其他方案）

### 新增的代码
- ✅ `.profile-header` 新头部容器
- ✅ `.cover-banner` 背景封面
- ✅ `.cover-gradient` 渐变背景
- ✅ `.profile-info-section` 信息区域
- ✅ `.avatar-wrapper` 头像容器
- ✅ `.user-details` 用户详情
- ✅ `.nickname` 昵称样式
- ✅ `.tags-row` 标签行
- ✅ `.tag-pill` 胶囊标签
- ✅ `.bio-text` 个性签名
- ✅ `.edit-profile-btn` 编辑按钮
- ✅ `.stats-bar` 统计栏
- ✅ `.stat-item` 统计项
- ✅ `.stat-number` 统计数字
- ✅ `.stat-label` 统计标签

---

## 🧪 测试验证

### 视觉检查清单
- [ ] 背景封面显示正常（140px 高度，三色渐变）
- [ ] 光晕效果可见（两个圆形径向渐变）
- [ ] 头像浮层效果（一半在背景上，一半在白色区域）
- [ ] 头像圆形完美（90px × 90px，border-radius: 50%）
- [ ] 白色边框清晰可见（4px solid white）
- [ ] 阴影柔和不突兀
- [ ] 昵称粗体清晰（20px，700）
- [ ] 专业标签胶囊样式正确（灰色圆角背景）
- [ ] 个性签名最多 2 行，超出省略
- [ ] 编辑资料按钮圆角边框样式
- [ ] 数据统计栏三个数字横向排列
- [ ] 统计数字粗体，标签灰色小字
- [ ] 分割线清晰可见

### 功能检查清单
- [ ] 点击"编辑资料"跳转到编辑页面
- [ ] 点击统计数字（作品/草稿/收藏）切换对应标签
- [ ] 头像显示上传的图片（如果有）
- [ ] 没有头像时显示首字母占位符
- [ ] 专业标签只在公开时显示
- [ ] 个性签名优先显示 bio，其次 signature

### 响应式检查
- [ ] 在不同手机屏幕上布局正常
- [ ] 文字不会溢出或重叠
- [ ] 头像和按钮对齐正确
- [ ] 统计栏在小屏幕上不会换行

---

## 🚀 后续优化建议

### 短期优化
1. **添加封面图自定义**：允许用户上传自己的封面图
2. **点击统计数字跳转**：点击"作品"数字直接切换到作品标签页
3. **添加动画效果**：页面加载时头像和信息的淡入动画
4. **优化占位符**：首字母占位符添加随机背景色

### 长期优化
1. **背景图多样化**：提供多种渐变主题供用户选择
2. **添加二维码**：在个人主页添加分享二维码
3. **社交链接**：添加微信、微博等社交链接
4. **作品合集**：类似小红书的"合集"功能
5. **浏览记录**：添加"我看过的"标签页

---

## 📸 设计参考

### 小红书个人主页特点
1. **大面积背景封面**：140-160px 高度
2. **头像浮层**：一半在背景上，一半在内容区
3. **信息简洁**：只显示昵称、签名、标签
4. **数据统计**：关注、粉丝、获赞横向排列
5. **白色内容区**：背景图下方改为白色，文字更清晰
6. **圆角按钮**：编辑资料按钮使用圆角边框

### 我们的实现
✅ 完全对标小红书的设计风格  
✅ 保持治愈系自然风配色（抹茶绿 + 柠檬黄）  
✅ 文字对比度充足（深色文字 + 白色背景）  
✅ 符合移动端设计规范  

---

**重构完成时间**: 2026-05-08  
**重构人员**: AI Assistant  
**参考设计**: 小红书个人主页（P2 截图）  
**设计风格**: 治愈系自然风 + 小红书布局
