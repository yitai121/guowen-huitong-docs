# 🌐 国文汇通 - 网站部署指南

## 📋 部署前准备

### 1. 确保文件结构完整
```
guowen-huitong/
├── assets/
│   ├── index.html          # 浏览页面（首页）
│   ├── admin.html          # 管理后台
│   └── guowen_huitong_data.json  # 资料数据
├── vercel.json             # Vercel 配置
├── netlify.toml            # Netlify 配置
├── CNAME                   # 域名配置（可选）
└── README.md               # 本文件
```

### 2. 准备域名（可选）
- 去域名注册商（阿里云、腾讯云、Namecheap 等）购买域名
- 建议使用简单易记的域名，如：`guowenhuitong.com`

---

## 🚀 快速部署方案

### 方案一：Vercel 部署（推荐 ⭐⭐⭐⭐⭐）

#### 优势
- ✅ 免费额度足够
- ✅ 自动 HTTPS
- ✅ 全球 CDN 加速
- ✅ 自动部署
- ✅ 自定义域名支持

#### 部署步骤

**1. 注册 Vercel 账号**
```
访问：https://vercel.com/signup
使用 GitHub、GitLab 或 Bitbucket 账号注册
```

**2. 安装 Vercel CLI**
```bash
# 全局安装
npm install -g vercel

# 或使用 npx（无需安装）
npx vercel
```

**3. 登录 Vercel**
```bash
vercel login
```

**4. 部署项目**
```bash
# 在项目根目录执行
vercel

# 按提示操作：
# - Set up and deploy? Y
# - Which scope? 选择你的账号
# - Link to existing project? N
# - Project name: guowen-huitong-docs
# - In which directory is your code located? ./
# - Override settings? N
```

**5. 生产环境部署**
```bash
vercel --prod
```

**6. 访问网站**
```
访问地址：https://guowen-huitong-docs.vercel.app
管理后台：https://guowen-huitong-docs.vercel.app/admin
```

**7. 绑定自定义域名**
```bash
# 在 Vercel 控制台添加域名
Settings -> Domains -> Add Domain

# 然后在域名 DNS 设置中添加 CNAME 记录：
# 主机记录：www
# 记录类型：CNAME
# 记录值：cname.vercel-dns.com
```

---

### 方案二：Netlify 部署（推荐 ⭐⭐⭐⭐）

#### 优势
- ✅ 免费额度慷慨
- ✅ 自动 HTTPS
- ✅ 表单处理
- ✅ 拖拽部署
- ✅ 边缘函数支持

#### 部署步骤

**1. 注册 Netlify 账号**
```
访问：https://app.netlify.com/signup
使用 GitHub、GitLab 或 Bitbucket 账号注册
```

**2. 拖拽部署（最简单）**
```
1. 访问：https://app.netlify.com/drop
2. 将 assets 文件夹拖拽到上传区域
3. 等待部署完成（几秒钟）
4. 获得访问地址：https://random-name.netlify.app
```

**3. Git 集成部署（推荐）**
```bash
# 1. 初始化 Git 仓库
git init
git add .
git commit -m "Initial commit"

# 2. 推送到 GitHub
# 在 GitHub 创建新仓库
git remote add origin https://github.com/your-username/guowen-huitong-docs.git
git push -u origin main

# 3. 在 Netlify 导入仓库
# 访问：https://app.netlify.com
# 点击 "New site from Git"
# 选择 GitHub 仓库
# 配置：
#   - Build command: (留空)
#   - Publish directory: assets
# 点击 "Deploy site"
```

**4. 访问网站**
```
访问地址：https://your-site-name.netlify.app
管理后台：https://your-site-name.netlify.app/admin
```

**5. 绑定自定义域名**
```
1. 在 Netlify 控制台：Domain settings -> Add custom domain
2. 添加你的域名
3. 在域名 DNS 设置中添加记录：
   - CNAME 记录：www -> your-site-name.netlify.app
   - A 记录：@ -> 75.2.70.75
```

---

### 方案三：GitHub Pages 部署（推荐 ⭐⭐⭐）

#### 优势
- ✅ 完全免费
- ✅ 与 GitHub 集成
- ✅ 自动 HTTPS
- ✅ 简单易用

#### 部署步骤

**1. 创建 GitHub 仓库**
```
1. 访问：https://github.com/new
2. 仓库名：guowen-huitong-docs
3. 设置为 Public
4. 点击 "Create repository"
```

**2. 上传文件**
```bash
# 方法1：使用 GitHub 上传功能
# 点击 "uploading an existing file"
# 拖拽所有文件上传

# 方法2：使用 Git 命令
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/guowen-huitong-docs.git
git push -u origin main
```

**3. 启用 GitHub Pages**
```
1. 进入仓库 Settings
2. 滚动到 "Pages" 部分
3. Source 选择：Deploy from a branch
4. Branch 选择：main
5. Folder 选择：/assets
6. 点击 "Save"
```

**4. 访问网站**
```
访问地址：https://your-username.github.io/guowen-huitong-docs/
管理后台：https://your-username.github.io/guowen-huitong-docs/admin
```

**5. 自定义域名**
```
1. 在 CNAME 文件中添加你的域名
2. 在域名 DNS 设置中添加 CNAME 记录：
   - www -> your-username.github.io
```

---

### 方案四：传统服务器部署（CPanel/宝塔面板）

#### 部署步骤

**1. 准备服务器**
```
- 购买虚拟主机或云服务器
- 获得 FTP 账号或控制面板登录信息
```

**2. 上传文件**
```
方法1：使用 FTP 工具（FileZilla）
- 连接到服务器
- 将 assets 文件夹内容上传到 public_html 目录

方法2：使用文件管理器（宝塔面板/CPanel）
- 登录控制面板
- 进入文件管理器
- 上传文件到网站根目录
```

**3. 配置域名**
```
1. 在域名 DNS 设置中添加 A 记录：
   - 主机记录：@ 或 www
   - 记录类型：A
   - 记录值：服务器 IP 地址

2. 等待 DNS 生效（10分钟 - 24小时）
```

**4. 访问网站**
```
访问地址：https://www.yourdomain.com
管理后台：https://www.yourdomain.com/admin
```

---

## 🔧 自定义域名配置

### 1. 购买域名
- 阿里云：https://wanwang.aliyun.com/
- 腾讯云：https://dnspod.cloud.tencent.com/
- Namecheap：https://www.namecheap.com/
- GoDaddy：https://www.godaddy.com/

### 2. 配置 DNS 解析

#### 域名解析记录示例
```
类型     主机记录        记录值                    TTL
CNAME    @              cname.vercel-dns.com       600
CNAME    www            cname.vercel-dns.com       600

# Netlify
CNAME    @              your-site-name.netlify.app  600
CNAME    www            your-site-name.netlify.app  600

# GitHub Pages
CNAME    www            your-username.github.io     600
A        @              185.199.108.153           600
A        @              185.199.109.153           600
A        @              185.199.110.153           600
A        @              185.199.111.153           600
```

### 3. 配置 HTTPS（免费）
- Vercel/Netlify/GitHub Pages 自动提供
- 传统服务器需要配置 Let's Encrypt

---

## 📊 部署平台对比

| 平台 | 免费额度 | 自定义域名 | 自动HTTPS | 全球CDN | 难度 | 推荐度 |
|------|---------|-----------|----------|---------|------|--------|
| Vercel | 100GB/月 | ✅ | ✅ | ✅ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Netlify | 100GB/月 | ✅ | ✅ | ✅ | ⭐ | ⭐⭐⭐⭐ |
| GitHub Pages | 1GB | ✅ | ✅ | ✅ | ⭐ | ⭐⭐⭐ |
| 阿里云OSS | 5GB | ✅ | 需配置 | ✅ | ⭐⭐⭐ | ⭐⭐⭐ |
| 腾讯云COS | 5GB | ✅ | 需配置 | ✅ | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 推荐部署方案

### 个人项目 / 小团队
**推荐：Vercel** 或 **Netlify**
- 免费额度充足
- 操作简单
- 全球访问速度快
- 自动部署

### 开源项目
**推荐：GitHub Pages**
- 完全免费
- 与 GitHub 集成
- 适合开源项目展示

### 企业项目
**推荐：自建服务器** 或 **云存储（阿里云OSS/腾讯云COS）**
- 数据安全
- 可控性强
- 支持大规模访问

---

## 🚦 部署后检查清单

### 1. 基础功能检查
- [ ] 访问首页是否正常显示
- [ ] 资料列表是否正确加载
- [ ] 搜索功能是否正常工作
- [ ] 下载功能是否可用
- [ ] 管理后台是否可以访问

### 2. 性能检查
- [ ] 页面加载速度（< 3秒）
- [ ] 图片是否正常显示
- [ ] 动画是否流畅
- [ ] 移动端是否正常显示

### 3. SEO 检查
- [ ] 网站标题是否正确
- [ ] Meta 描述是否完整
- [ ] 是否有合适的关键词
- [ ] Favicon 是否显示

### 4. 安全检查
- [ ] 是否启用 HTTPS
- [ ] 安全头是否设置
- [ ] 是否有 XSS 防护
- [ ] 管理后台是否需要密码保护

---

## 📞 常见问题

### Q1: 部署后页面显示 404
**A:** 检查以下几点：
- 文件是否上传到正确目录
- 路径是否正确（/assets/）
- 是否配置了正确的路由重定向

### Q2: 自定义域名无法访问
**A:** 检查 DNS 设置：
- DNS 记录是否正确添加
- 是否等待了 DNS 生效时间
- 域名是否正确指向服务器

### Q3: HTTPS 无法启用
**A:** 确认：
- 域名 DNS 已正确解析
- 部署平台是否支持自动 HTTPS
- 是否配置了正确的 SSL 证书

### Q4: 加载速度慢
**A:** 优化方案：
- 压缩图片
- 使用 CDN 加速
- 启用 Gzip 压缩
- 减少 HTTP 请求

---

## 🎨 网站推广

### 1. SEO 优化
- 提交到搜索引擎（百度站长平台、Google Search Console）
- 优化 Meta 标签和关键词
- 创建 sitemap.xml
- 提交到目录网站

### 2. 社交媒体
- 分享到微信、微博、Twitter
- 创建官方公众号
- 发布相关内容

### 3. 其他渠道
- 行业论坛推广
- 合作伙伴推广
- 内容营销

---

## 📈 监控和维护

### 1. 访问统计
- 部署平台自带统计
- 集成 Google Analytics
- 使用百度统计

### 2. 错误监控
- 使用 Sentry 监控错误
- 定期检查网站日志
- 及时修复 bug

### 3. 定期更新
- 更新资料内容
- 优化页面性能
- 修复安全漏洞

---

## 🎉 完成部署！

部署完成后，你将拥有：
- ✅ 一个专业的资料管理系统
- ✅ 可以公开访问的网站
- ✅ 自定义域名
- ✅ HTTPS 加密
- ✅ 全球 CDN 加速
- ✅ 自动化部署

**开始推广你的网站吧！** 🚀

---

**技术支持：**
- Vercel 文档：https://vercel.com/docs
- Netlify 文档：https://docs.netlify.com/
- GitHub Pages 文档：https://docs.github.com/pages

**祝你部署成功！** 💪
