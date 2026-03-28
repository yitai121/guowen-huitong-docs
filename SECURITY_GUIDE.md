# 🔒 安全配置方案 - 保护你的网站

<div align="center">

**确保你的网站安全可靠**

**预计时间：10分钟**

[安全现状](#安全现状) • [安全加固](#安全加固) • [备份方案](#备份方案) • [监控告警](#监控告警)

</div>

---

## ✅ 安全现状

### 你的网站已经具备的安全措施

**Vercel 自动提供的：**
- ✅ **HTTPS 加密** - 自动 SSL 证书
- ✅ **DDoS 防护** - 防止攻击
- ✅ **防火墙** - 阻止恶意访问
- ✅ **全球 CDN** - 加速且安全
- ✅ **自动更新** - 安全补丁自动更新

**我们的网站：**
- ✅ 纯静态网站 - 没有数据库攻击风险
- ✅ 没有用户登录 - 降低攻击面
- ✅ 使用 HTTPS - 数据传输加密

### 安全风险

**潜在风险：**
- ⚠️ 管理后台没有密码保护
- ⚠️ 任何人都可以访问管理后台
- ⚠️ 域名被劫持风险
- ⚠️ DNS 污染风险

---

## 🔒 安全加固

### 方案1：修改管理后台地址

**原理：**
- 不使用常见的 `/admin`
- 使用复杂的管理后台地址
- 降低被发现的概率

**步骤：**

**方法A：修改配置文件**
```json
// vercel.json
{
  "rewrites": [
    {
      "source": "/admin-secret-2026",
      "destination": "/admin.html"
    }
  ]
}
```

**方法B：重命名文件**
```bash
# 将 admin.html 重命名为 admin-secret-2024.html
mv assets/admin.html assets/admin-secret-2026.html
```

**访问地址：**
- 旧地址：`https://www.guowenhuitong.com/admin`
- 新地址：`https://www.guowenhuitong.com/admin-secret-2024`

**建议：**
- 使用复杂的地址
- 定期更换
- 不要在公开场合透露

### 方案2：启用 HTTP 严格传输安全（HSTS）

**原理：**
- 强制浏览器使用 HTTPS
- 防止降级攻击

**步骤：**

在 `netlify.toml` 中添加：
```toml
[[headers]]
  for = "/*"
  [headers.values]
    Strict-Transport-Security = "max-age=31536000; includeSubDomains; preload"
```

### 方案3：设置安全响应头

**在 `netlify.toml` 中添加：**
```toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    X-XSS-Protection = "1; mode=block"
    Referrer-Policy = "strict-origin-when-cross-origin"
```

### 方案4：保护敏感数据

**注意事项：**
- ❌ 不要在代码中存储密码
- ❌ 不要在前端存储敏感信息
- ❌ 不要在 URL 中传递敏感数据

**正确做法：**
- ✅ 使用环境变量
- ✅ 使用后端API
- ✅ 加密敏感数据

### 方案5：限制访问频率

**原理：**
- 防止暴力破解
- 防止恶意爬虫

**步骤：**

在 `vercel.json` 中添加：
```json
{
  "routes": [
    {
      "src": "/(.*)",
      "headers": {
        "X-RateLimit-Limit": "1000",
        "X-RateLimit-Remaining": "999",
        "X-RateLimit-Reset": "3600"
      }
    }
  ]
}
```

---

## 💾 备份方案

### 为什么需要备份？

**备份的作用：**
- 🔄 网站被攻击后可以恢复
- 🔄 误删文件可以恢复
- 🔄 更新失败可以回滚

### 备份策略

**方案1：Git 自动备份**

**优点：**
- ✅ 免费
- ✅ 版本控制
- ✅ 容易恢复

**步骤：**
```bash
# 1. 初始化 Git 仓库
git init

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "Backup: $(date)"

# 4. 推送到 GitHub
git push origin main
```

**定时备份脚本：**
```bash
#!/bin/bash
# 每天自动备份脚本

# 进入项目目录
cd /path/to/project

# 拉取最新代码
git pull

# 添加所有文件
git add .

# 提交
git commit -m "Auto backup: $(date)"

# 推送
git push origin main
```

**方案2：手动备份**

**步骤：**
1. 定期下载所有文件
2. 保存到多个位置：
   - 电脑硬盘
   - U盘
   - 云盘（百度云、阿里云盘）

**备份频率：**
- 更新频繁：每天备份
- 更新不频繁：每周备份
- 重要内容：实时备份

### 数据备份

**备份 `guowen_huitong_data.json`：**
```bash
# 复制数据文件
cp assets/guowen_huitong_data.json backup/guowen_huitong_data_$(date +%Y%m%d).json
```

---

## 📊 监控告警

### 为什么要监控？

**监控的作用：**
- 🔍 及时发现问题
- 🔍 了解网站访问情况
- 🔍 分析用户行为

### 监控工具

**工具1：Vercel Analytics**

**优点：**
- ✅ 免费
- ✅ 集成在 Vercel
- ✅ 实时数据

**步骤：**
1. 登录 Vercel Dashboard
2. 选择你的项目
3. 点击"Analytics"
4. 查看访问数据

**工具2：百度统计**

**优点：**
- ✅ 免费
- ✅ 适合国内网站
- ✅ 功能强大

**步骤：**
1. 访问：https://tongji.baidu.com/
2. 注册账号
3. 添加网站
4. 复制统计代码
5. 添加到 `index.html` 的 `<head>` 部分

**工具3：Google Analytics**

**优点：**
- ✅ 免费
- ✅ 全球通用
- ✅ 功能强大

**步骤：**
1. 访问：https://analytics.google.com/
2. 注册账号
3. 创建账号
4. 添加网站
5. 复制追踪代码
6. 添加到 `index.html` 的 `<head>` 部分

### 告警设置

**设置告警通知：**

**方式1：邮件通知**
- Vercel 自动发送邮件
- 配置邮箱接收通知

**方式2：短信通知**
- 需要第三方服务
- 比如：Server酱、阿里云短信

---

## 🛡️ 安全检查清单

### 每月检查：

- [ ] 网站是否正常运行
- [ ] HTTPS 是否正常
- [ ] 域名是否即将过期
- [ ] 备份是否完成
- [ ] 是否有异常访问

### 每季度检查：

- [ ] 安全配置是否需要更新
- [ ] 依赖包是否有漏洞
- [ ] DNS 解析是否正常
- [ ] SSL 证书是否即将过期
- [ ] 代码是否有安全漏洞

### 每年检查：

- [ ] 域名是否需要续费
- [ ] 账号密码是否需要更换
- [ ] 备份策略是否需要更新
- [ ] 安全方案是否需要升级

---

## ⚠️ 常见安全问题

### Q1: 网站被黑了怎么办？

**A:** 立即执行：
1. 检查代码是否有修改
2. 从备份恢复
3. 查找漏洞
4. 加强安全措施
5. 更新所有密码

### Q2: 域名被劫持了怎么办？

**A:** 立即执行：
1. 联系域名注册商
2. 提供身份证明
3. 修改 DNS 解析
4. 启用域名锁
5. 更改域名密码

### Q3: 数据丢失了怎么办？

**A:** 立即执行：
1. 检查备份
2. 从备份恢复
3. 检查丢失原因
4. 加强备份策略

### Q4: 网站访问很慢怎么办？

**A:** 检查：
1. CDN 是否正常
2. 文件是否过大
3. 图片是否优化
4. DNS 是否正常

---

## 🎉 总结

### 你需要做的安全措施：

**立即执行（1小时）：**
1. ✅ 修改管理后台地址
2. ✅ 启用 HTTPS
3. ✅ 设置安全响应头
4. ✅ 创建备份计划

**定期执行（每周）：**
1. ✅ 检查网站运行状态
2. ✅ 备份数据
3. ✅ 查看访问日志
4. ✅ 检查安全更新

**持续执行（每天）：**
1. ✅ 监控网站访问
2. ✅ 检查异常行为
3. ✅ 更新内容
4. ✅ 维护备份

---

**下一步：**
- 查看 [QUICK_START.md](./QUICK_START.md) 开始部署
- 查看 [SEO_GUIDE.md](./SEO_GUIDE.md) 优化搜索

---

**最后更新：2024年1月26日**
