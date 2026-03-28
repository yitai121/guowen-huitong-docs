# 国文汇通网站部署指南

域名：gwht.cc

## 📋 部署步骤

### 第一步：启用 GitHub Pages

1. 访问 GitHub 仓库：https://github.com/yitai121/guowen-huitong-docs
2. 点击 **Settings** 标签
3. 在左侧菜单中找到 **Pages**
4. 在 "Source" 部分，选择：
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/(root)**
5. 点击 **Save**
6. 等待 1-2 分钟，页面会显示部署成功

### 第二步：配置 DNS

登录你的域名服务商（阿里云、腾讯云、Cloudflare 等），添加以下 DNS 记录：

#### 选项 1：使用 GitHub Pages（推荐，免费）

```
记录类型: CNAME
主机记录: @
记录值: yitai121.github.io
TTL: 600
```

#### 选项 2：使用 Vercel（需要 Vercel 账户）

如果你使用 Vercel 部署，DNS 配置为：

```
记录类型: CNAME
主机记录: @
记录值: guowen-huitong-docs.vercel.app
TTL: 600
```

### 第三步：等待 DNS 生效

DNS 生效时间：**10 分钟 - 24 小时**

#### 检查 DNS 是否生效：

**Windows**：
```bash
nslookup gwht.cc
```

**Mac/Linux**：
```bash
dig gwht.cc
```

如果看到返回的 IP 地址，说明 DNS 已生效。

### 第四步：验证网站

DNS 生效后，访问：

- 主页：https://gwht.cc
- 管理后台：https://gwht.cc/admin.html

---

## 🔐 管理员登录信息

- 用户名：`admin`
- 密码：`admin888`

---

## 📂 项目文件说明

```
gwht.cc/
├── index.html              # 主页
├── admin.html              # 管理后台
├── vercel.json             # Vercel 配置
├── CNAME                   # 域名配置（指向 gwht.cc）
├── README.md               # 项目说明
├── assets/
│   ├── admin/
│   │   ├── dashboard.html  # 管理仪表板
│   │   └── login.html      # 登录页
│   └── js/
│       └── security-config.js  # 安全配置
```

---

## 🚀 常见问题

### Q1: DNS 生效后还是访问不了？

**A**: 请检查以下几点：
1. DNS 记录是否正确配置
2. 是否已启用 GitHub Pages
3. 等待时间是否足够（最多 24 小时）
4. 尝试清除浏览器缓存

### Q2: 管理后台打不开？

**A**: 确保访问的是：
- https://gwht.cc/admin.html
- 不是 https://gwht.cc/admin

### Q3: 如何查看 GitHub Pages 部署状态？

**A**:
1. 访问仓库的 Settings → Pages
2. 查看顶部显示的部署状态
3. 如果显示失败，点击 "View deployment" 查看日志

### Q4: 如何查看默认域名？

**A**: GitHub Pages 默认域名：
- https://yitai121.github.io/guowen-huitong-docs/

如果域名配置有问题，可以先使用这个地址访问。

---

## 📞 技术支持

如果遇到问题，请检查：
1. GitHub 仓库：https://github.com/yitai121/guowen-huitong-docs
2. GitHub Pages 设置：Settings → Pages
3. DNS 配置：登录域名服务商查看

---

**部署完成后，网站将在 10 分钟 - 24 小时内生效！**
