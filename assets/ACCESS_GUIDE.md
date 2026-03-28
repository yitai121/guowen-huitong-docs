# 🌐 国文汇通 - 完整访问指南

## 📍 网站访问地址

### 🌍 本地开发环境
**用于开发和测试**

**浏览页面：**
```
http://localhost:8000/index.html
或
assets/index.html
```

**管理后台：**
```
http://localhost:8000/admin.html
或
assets/admin.html
```

### 🌐 生产环境（部署后）

#### 方案1：Vercel 部署
**浏览页面：**
```
https://guowen-huitong-docs.vercel.app
或
https://www.yourdomain.com  (自定义域名)
```

**管理后台：**
```
https://guowen-huitong-docs.vercel.app/admin
或
https://www.yourdomain.com/admin
```

#### 方案2：Netlify 部署
**浏览页面：**
```
https://your-site-name.netlify.app
或
https://www.yourdomain.com
```

**管理后台：**
```
https://your-site-name.netlify.app/admin
或
https://www.yourdomain.com/admin
```

#### 方案3：GitHub Pages 部署
**浏览页面：**
```
https://your-username.github.io/guowen-huitong-docs/
或
https://www.yourdomain.com
```

**管理后台：**
```
https://your-username.github.io/guowen-huitong-docs/admin
或
https://www.yourdomain.com/admin
```

#### 方案4：自定义域名
**浏览页面：**
```
https://www.guowenhuitong.com
```

**管理后台：**
```
https://www.guowenhuitong.com/admin
```

---

## 🚀 快速部署（获得 www. 域名）

### 推荐方案：Vercel（最简单）⭐⭐⭐⭐⭐

#### 步骤1：注册账号
```
访问：https://vercel.com/signup
使用 GitHub 账号注册（推荐）
```

#### 步骤2：安装 Vercel CLI
```bash
# 全局安装
npm install -g vercel

# 或直接使用 npx（无需安装）
npx vercel
```

#### 步骤3：登录
```bash
vercel login
```

#### 步骤4：部署项目
```bash
# 在项目根目录执行
vercel

# 按提示操作：
# - Set up and deploy? Y
# - Project name: guowen-huitong-docs
```

#### 步骤5：生产环境部署
```bash
vercel --prod
```

#### 步骤6：获得访问地址
```
浏览页面：https://guowen-huitong-docs.vercel.app
管理后台：https://guowen-huitong-docs.vercel.app/admin
```

#### 步骤7：绑定自定义域名（可选）
```
1. 访问：https://vercel.com/dashboard
2. 选择你的项目
3. 进入 Settings -> Domains
4. 添加域名：www.guowenhuitong.com
5. 在域名 DNS 设置中添加 CNAME 记录：
   - 主机记录：www
   - 记录类型：CNAME
   - 记录值：cname.vercel-dns.com
6. 等待 DNS 生效（10分钟 - 24小时）
```

### 详细部署教程：查看 [DEPLOY.md](./DEPLOY.md)

---

## 💡 使用指南

### 🔹 作为普通用户（浏览资料）

#### 1. 打开浏览页面
在浏览器中访问：
```
https://www.yourdomain.com
```

#### 2. 搜索资料
- 在搜索框输入关键词
- 点击分类标签筛选
- 点击"搜索"按钮

#### 3. 查看详情
- 点击"详情"按钮查看完整信息
- 查看描述、标签、大小等信息

#### 4. 下载资料
- 点击"下载"按钮
- 获取 24 小时有效链接
- 开始下载

---

### 🔹 作为管理员（管理资料）

#### 1. 打开管理后台
在浏览器中访问：
```
https://www.yourdomain.com/admin
```

#### 2. 上传新资料
1. 点击"上传新资料"按钮
2. 填写资料信息：
   - **标题**（必填）：资料名称
   - **文件路径/URL**（必填）：文件地址
   - **分类**（必填）：选择分类
   - **标签**（可选）：用逗号分隔
   - **文件大小**（可选）：单位 MB
   - **描述**（可选）：资料说明
3. 点击"上传资料"完成

#### 3. 编辑资料
1. 在资料列表中找到目标资料
2. 点击"编辑"按钮
3. 修改信息
4. 点击"保存修改"

#### 4. 上架/下架资料
1. 在资料列表中找到目标资料
2. 点击"上架"或"下架"按钮
3. 确认操作

#### 5. 批量操作
1. 勾选多个资料
2. 使用批量操作按钮：
   - 批量上架
   - 批量下架
   - 批量删除

#### 6. 删除资料
1. 在资料列表中找到目标资料
2. 点击"删除"按钮
3. 确认删除

⚠️ **警告：删除后无法恢复！**

---

## 📊 功能说明

### 浏览页面功能
- ✅ 资料搜索
- ✅ 分类筛选
- ✅ 资料浏览
- ✅ 详情查看
- ✅ 资料下载
- ✅ 数据统计
- ✅ 丝滑动画
- ✅ 响应式设计

### 管理后台功能
- ✅ 资料上传
- ✅ 资料编辑
- ✅ 资料上架
- ✅ 资料下架
- ✅ 资料删除
- ✅ 批量操作
- ✅ 搜索筛选
- ✅ 数据统计
- ✅ 分类管理

---

## 🎯 资料状态说明

### ✅ 已上架（active）
- 在浏览页面**可见**
- 可以被**搜索**到
- 可以被**下载**

### ❌ 已下架（inactive）
- 在浏览页面**隐藏**
- **无法**被搜索到
- **无法**被下载

---

## 🔍 搜索技巧

### 1. 关键词搜索
- 使用多个关键词提高精确度
- 搜索标题、描述、标签
- 支持模糊匹配

### 2. 分类筛选
- 点击分类标签
- 快速找到特定分类资料
- 可与关键词组合使用

### 3. 组合搜索
- 同时使用关键词和分类
- 精确定位目标资料
- 提高搜索效率

---

## 📈 数据统计

### 浏览页面统计
- 总文档数
- 总存储空间
- 总下载次数
- 分类数量

### 管理后台统计
- 总资料数
- 已上架数
- 已下架数
- 总存储空间
- 总下载次数

---

## 🎨 界面特色

### 浏览页面
- 🌈 深色渐变主题
- ✨ 丝滑动画效果
- 📱 响应式设计
- 🎯 简洁易用
- 🔍 智能搜索
- 📊 实时统计

### 管理后台
- 📊 专业的管理界面
- 📋 清晰的数据表格
- 🔍 强大的搜索筛选
- ⚡ 高效的操作流程
- 🔄 批量操作支持
- 📈 实时数据更新

---

## 🔐 安全建议

### 1. 管理后台安全
- 定期修改访问密码（如有）
- 限制访问 IP（如需要）
- 使用 HTTPS 加密
- 启用双重验证（如支持）

### 2. 资料安全
- 定期备份数据
- 敏感资料注意权限控制
- 监控下载行为
- 及时清理无用资料

### 3. 网站安全
- 启用 HTTPS
- 定期更新
- 监控访问日志
- 防止恶意攻击

---

## 📞 技术支持

### 常见问题
详见 [DEPLOY.md](./DEPLOY.md) 中的常见问题部分

### 获取帮助
- 查看 [DEPLOY.md](./DEPLOY.md) 详细部署教程
- 查看部署平台文档（Vercel/Netlify）
- 查看项目 README.md

---

## 🎉 开始使用

### 立即体验
1. 打开 `assets/index.html` 查看浏览页面
2. 打开 `assets/admin.html` 管理资料

### 部署上线
1. 选择部署平台（推荐 Vercel）
2. 按照 [DEPLOY.md](./DEPLOY.md) 部署
3. 绑定自定义域名
4. 开始推广！

---

## 📝 备忘录

### 重要链接
- 浏览页面：`/` 或 `/index.html`
- 管理后台：`/admin` 或 `/admin.html`
- 部署教程：[DEPLOY.md](./DEPLOY.md)

### 快捷操作
- 上传资料：管理后台 → 上传新资料
- 搜索资料：浏览页面 → 搜索框
- 下载资料：浏览页面 → 下载按钮
- 管理资料：管理后台 → 资料列表

---

**享受丝滑的资料管理体验！** 🚀📚✨
