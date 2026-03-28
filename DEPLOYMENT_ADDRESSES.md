# 🌐 国文汇通资料管理系统 - 部署地址文档

## 📍 访问地址

### 公开访问地址
- **主站地址**: `https://www.guowenhuitong.com`
- **资料浏览**: `https://www.guowenhuitong.com/`
- **文档下载**: `https://www.guowenhuitong.com/`

### 管理员入口（隐藏）
- **管理员登录**: `https://www.guowenhuitong.com/admin`
- **管理后台**: `https://www.guowenhuitong.com/admin/dashboard`

⚠️ **重要提示**:
- 管理员入口对外不呈现，无直接链接
- 需要知道具体地址才能访问
- 登录页面有密码保护
- 会话有效期：24 小时

---

## 🔐 管理员登录凭据

### 默认管理员账号
- **用户名**: `admin`
- **密码**: `admin888`

⚠️ **安全提示**:
- 首次登录后请立即修改密码
- 生产环境务必更换默认密码
- 建议使用强密码（至少8位，包含大小写字母、数字和特殊字符）

---

## 🚀 部署平台

### Vercel 部署
- **部署地址**: `https://guwen-huitong-docs.vercel.app`
- **自定义域名**: `https://www.guowenhuitong.com`
- **状态**: ✅ 已配置

### Netlify 部署
- **部署地址**: `https://guwen-huitong-docs.netlify.app`
- **自定义域名**: `https://www.guowenhuitong.com`
- **状态**: ✅ 已配置

---

## 📋 域名配置

### DNS 记录
```
类型: CNAME
名称: www
值: guwen-huitong-docs.vercel.app (或你的 Netlify 域名)
TTL: 3600
```

### SSL/TLS 证书
- ✅ 已启用自动 HTTPS
- ✅ SSL 证书已配置
- ✅ 强制 HTTPS 重定向

---

## 🛡️ 安全配置

### 已实现的安全措施

#### 1. CSP（内容安全策略）
- 默认策略：仅允许同源资源
- 脚本：允许内联脚本和动态脚本
- 样式：允许内联样式
- 图片：允许 data、https、http
- 禁止：外部框架嵌入

#### 2. 安全头部
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: no-referrer-when-downgrade`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`

#### 3. XSS 防护
- HTML 转义
- URL 净化
- CSP 限制
- 输入验证

#### 4. CSRF 保护
- CSRF 令牌生成
- 会话令牌验证
- 同站 Cookie 策略

#### 5. 加密
- SHA-256 密码哈希
- Base64 编码/解码
- 会话数据加密
- 随机令牌生成

---

## 🔧 访问流程

### 普通用户访问
1. 访问 `https://www.guowenhuitong.com`
2. 浏览资料列表
3. 搜索和筛选资料
4. 下载所需资料
5. 联系客服（如果需要）

### 管理员访问
1. 访问 `https://www.guowenhuitong.com/admin`
2. 输入用户名和密码
3. 验证成功后跳转到管理后台
4. 进行资料管理、配置设置等操作
5. 操作完成后退出登录

---

## 📊 功能模块

### 公开功能
- ✅ 资料浏览
- ✅ 搜索筛选
- ✅ 分类浏览
- ✅ 资料下载
- ✅ 客服咨询
- ✅ 响应式设计

### 管理功能
- ✅ 资料上传
- ✅ 资料编辑
- ✅ 资料删除
- ✅ 批量操作
- ✅ 站点配置
- ✅ 客服配置
- ✅ 邀请码配置
- ✅ 数据统计

---

## 🔍 文件路径映射

### 资源路径
```
/ → assets/index.html
/admin → assets/admin/login.html
/admin/dashboard → assets/admin/dashboard.html
```

### 配置文件
```
/site_config.json → assets/site_config.json
/guowen_huitong_data.json → assets/guowen_huitong_data.json
/js/security-config.js → assets/js/security-config.js
```

---

## 📱 移动端访问

### 响应式断点
- **手机**: < 768px
- **平板**: 768px - 1024px
- **桌面**: > 1024px

### 移动端优化
- ✅ 触摸友好
- ✅ 自适应布局
- ✅ 快速加载
- ✅ 流畅动画

---

## 🚨 故障排查

### 无法访问网站
1. 检查网络连接
2. 清除浏览器缓存
3. 尝试其他浏览器
4. 检查域名 DNS 解析

### 无法登录后台
1. 确认访问地址正确：`/admin`
2. 检查用户名和密码
3. 清除浏览器缓存和 Cookie
4. 尝试无痕模式

### 配置不生效
1. 检查 `site_config.json` 文件
2. 确认保存成功
3. 刷新页面
4. 清除浏览器缓存

---

## 📞 技术支持

### 联系方式
- **客服1**: 二维码扫码
- **客服2**: 二维码扫码
- **工作时间**: 7×24小时在线

### 常见问题
查看系统内的帮助文档或联系客服。

---

## ✨ 版本信息

- **当前版本**: v3.0
- **发布日期**: 2024年
- **最后更新**: 2024年
- **状态**: ✅ 正常运行

---

## 📝 更新日志

### v3.0 (2024年)
- ✅ 隐藏管理员入口
- ✅ 增强安全配置
- ✅ 添加后端加密
- ✅ 升级视觉设计
- ✅ 优化用户体验

### v2.0
- ✅ 添加客服系统
- ✅ 配置邀请码
- ✅ 响应式设计

### v1.0
- ✅ 基础功能实现

---

**部署状态**: ✅ 已完成
**访问地址**: https://www.guowenhuitong.com
**管理员入口**: https://www.guowenhuitong.com/admin
