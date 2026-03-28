# 🍎 Mac M 芯片专属部署指南

## 📋 部署前准备

### 你需要准备的信息（4 项）

1. ✅ **GitHub 用户名** - 你的 GitHub 账号名称
2. ✅ **GitHub 邮箱** - 你注册 GitHub 时用的邮箱
3. ✅ **GitHub Token** - 一个访问令牌（稍后教你怎么获取）
4. ✅ **你的名字** - 用于 Git 提交时显示

---

## 🎯 第一步：获取 GitHub Token（2 分钟）

### 1.1 打开 GitHub Token 设置页面
在浏览器地址栏输入并回车：
```
https://github.com/settings/tokens
```

### 1.2 生成新的 Token
1. 点击右上角的绿色按钮：`Generate new token`
2. 选择：`Generate new token (classic)`

### 1.3 配置 Token
填写以下信息：
- **Note**: 输入 `guowen-deploy`（用于标识这个 Token 的用途）
- **Expiration**: 选择 `90 days` 或 `No expiration`（不过期）
- **Select scopes**（权限）：
  - 勾选 `repo`（这会自动选中所有子选项）
  - 确保以下都被勾选：
    - ✓ repo:status
    - ✓ repo_deployment
    - ✓ public_repo
    - ✓ repo:invite
    - ✓ security_events

### 1.4 生成并复制 Token
1. 滚动到页面底部
2. 点击绿色按钮：`Generate token`
3. **重要！** 会看到一行以 `ghp_` 开头的字符串
4. **立即复制**这个 Token（只会显示一次！）
5. 建议保存到备忘录

---

## 🖥️ 第二步：编辑部署脚本（1 分钟）

### 2.1 打开终端
- 按 `Command + 空格` 打开 Spotlight 搜索
- 输入 `终端` 或 `Terminal`
- 按回车打开

### 2.2 进入项目目录
在终端中输入：
```bash
cd /workspace/projects
```

按回车。

### 2.3 编辑配置文件
在终端中输入：
```bash
nano mac_deploy.sh
```

按回车。

### 2.4 填写配置信息
你会看到一个文本编辑器，使用方向键移动光标到第 10-15 行，填写以下信息：

```bash
# 原始内容（示例）
GITHUB_USERNAME=""           # 改成你的用户名
GITHUB_REPO_NAME="guowen-huitong-docs"  # 可以不改
GITHUB_EMAIL=""              # 改成你的邮箱
GITHUB_TOKEN=""              # 粘贴刚才复制的 Token
GIT_NAME=""                  # 改成你的名字
```

**填写示例：**
```bash
GITHUB_USERNAME="zhangsan"           # 你的 GitHub 用户名
GITHUB_REPO_NAME="guowen-huitong-docs"
GITHUB_EMAIL="zhangsan@example.com"  # 你的 GitHub 邮箱
GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxx"  # 刚才复制的 Token
GIT_NAME="张三"                      # 你的名字
```

**注意事项：**
- 保留引号 `""`
- Token 不要有多余的空格
- 确保所有值都填写完整

### 2.5 保存并退出
1. 按 `Ctrl + O`（字母 O，不是数字 0）
2. 按回车确认保存
3. 按 `Ctrl + X` 退出编辑器

---

## 🚀 第三步：运行部署脚本（1 分钟）

### 3.1 给脚本添加执行权限
在终端中输入：
```bash
chmod +x mac_deploy.sh
```

按回车。

### 3.2 运行脚本
在终端中输入：
```bash
bash mac_deploy.sh
```

按回车。

### 3.3 观察执行过程
你会看到脚本自动执行以下步骤：

```
╔══════════━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━══════════━━━━━━━━═══╗
║           🚀 国文汇通 - Mac M 芯片自动化部署                  ║
╚════════━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━═══╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  检查配置信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 配置信息检查通过

配置信息预览：
  GitHub 用户名: zhangsan
  GitHub 邮箱:   zhangsan@example.com
  仓库名称:      guowen-huitong-docs
  你的名字:      张三
  Token:         ghp_xxxxxxxx... (已脱敏)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  检查 Git 环境
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Git 已安装: git version 2.x.x

... (继续执行)
```

### 3.4 等待完成
脚本会自动执行以下操作：
1. ✅ 检查配置信息
2. ✅ 检查 Git 环境
3. ✅ 初始化 Git 仓库
4. ✅ 配置 Git 用户信息
5. ✅ 添加所有文件
6. ✅ 提交代码
7. ✅ 创建 GitHub 仓库
8. ✅ 配置远程仓库
9. ✅ 推送代码到 GitHub

整个过程大约需要 1-2 分钟。

### 3.5 看到成功提示
如果一切顺利，你会看到：
```
🎉 自动部署第一步完成！

═══════════════════════════════════════════════════
📦 你的 GitHub 仓库：
   https://github.com/zhangsan/guowen-huitong-docs
═══════════════════════════════════════════════════
```

---

## 🌐 第四步：在 Vercel 部署（3 分钟）

### 4.1 访问 Vercel
在浏览器中访问：
```
https://vercel.com
```

### 4.2 登录 Vercel
1. 点击右上角的 `Login` 按钮
2. 选择 `Continue with GitHub`
3. 使用你的 GitHub 账号登录
4. 可能需要授权 Vercel 访问你的 GitHub 仓库

### 4.3 导入项目
1. 登录后，点击页面上的 `Add New Project` 按钮
2. 滚动页面，找到 `Your GitHub Repositories` 部分
3. 找到你的 `guowen-huitong-docs` 仓库
4. 点击仓库卡片上的 `Import` 按钮

### 4.4 配置项目
导入后，你会看到项目配置页面：
- **Project Name**: `guowen-huitong-docs`（可以不改）
- **Framework Preset**: `Other`（自动检测）
- **Root Directory**: `./`（可以不改）

**保持默认设置，直接下一步。**

### 4.5 开始部署
1. 滚动到底部
2. 点击蓝色的 `Deploy` 按钮
3. 等待部署过程（约 1-2 分钟）

### 4.6 部署完成
看到 `Congratulations!` 页面就表示部署成功了！

Vercel 会给你一个预览链接，例如：
```
https://guwen-huitong-docs.vercel.app
```

### 4.7 访问你的网站
1. 点击域名链接
2. 你会看到全新的国文汇通网站
3. 背景有浮动的彩色球体和粒子效果
4. 界面是现代化的玻璃态设计

---

## 🌟 第五步：绑定自定义域名（可选，10 分钟）

如果你想使用 `www.guowenhuitong.com` 作为域名，可以按以下步骤操作：

### 5.1 在 Vercel 添加域名
1. 回到 Vercel 项目页面
2. 点击顶部的 `Settings` 标签
3. 点击左侧菜单的 `Domains`
4. 在输入框中输入：`www.guowenhuitong.com`
5. 点击 `Add` 按钮

### 5.2 配置 DNS（推荐使用 Vercel DNS）
1. 添加域名后，Vercel 会提示配置 DNS
2. 点击 `Configure DNS` 按钮
3. 选择 `Use Vercel DNS`（最简单的方式）
4. 按照页面提示操作
5. 等待 DNS 生效（通常 10-30 分钟）

### 5.3 验证域名
- 在浏览器访问：`https://www.guowenhuitong.com`
- 看到你的网站就表示配置成功

---

## ✅ 验证部署成功

### 检查清单

- [ ] 本地预览：`http://localhost:8000` 能看到新界面
- [ ] Vercel 域名：`https://guwen-huitong-docs.vercel.app` 能正常访问
- [ ] 自定义域名：`https://www.guowenhuitong.com` 能正常访问（如果配置了）
- [ ] 管理员登录：`https://www.guowenhuitong.com/admin/login.html` 能看到登录页
- [ ] 能用 `admin`/`admin888` 登录管理后台

---

## 🎨 新界面特征（确认是否是最新版本）

### 首页特征
✅ 背景有浮动的彩色球体（紫色、粉色、蓝色）
✅ 有漂浮的白色小粒子
✅ 标题是"让知识管理变得简单高效"
✅ 卡片是毛玻璃效果（半透明模糊）
✅ 按钮是紫蓝粉渐变色
✅ 鼠标悬停有动画效果

### 管理员登录页特征
✅ 背景有网格线
✅ 有浮动的彩色球体
✅ Logo 有脉冲呼吸效果
✅ 卡片是毛玻璃效果
✅ 输入框是半透明的

### 管理后台特征
✅ 统计卡片有渐变边框
✅ 表格是现代化的
✅ 整体风格与首页一致

---

## 🆘 常见问题

### Q1: 提示 "GITHUB_TOKEN 未填写"
**解决方法：**
1. 重新运行 `nano mac_deploy.sh`
2. 确认第 14 行的 `GITHUB_TOKEN` 已填写
3. 确认 Token 是以 `ghp_` 开头的完整字符串
4. 保存后重新运行脚本

### Q2: 提示 "Git 未安装"
**解决方法：**
Mac 通常预装了 Git，如果没有：
```bash
xcode-select --install
```
按提示安装 Xcode Command Line Tools。

### Q3: 提示 "GitHub 仓库创建失败"
**可能原因：**
1. Token 权限不足（需要 `repo` 权限）
2. 仓库名称已存在
3. 网络连接问题

**解决方法：**
1. 检查 Token 是否勾选了 `repo` 权限
2. 如果仓库名称已存在，脚本会自动使用现有仓库
3. 检查网络连接，重试脚本

### Q4: 推送代码失败
**可能原因：**
1. Token 已过期或无效
2. 网络连接问题
3. 仓库配置错误

**解决方法：**
1. 重新生成 GitHub Token
2. 更新脚本中的 Token
3. 重新运行脚本

### Q5: Vercel 部署失败
**可能原因：**
1. GitHub 仓库为空
2. 构建配置错误

**解决方法：**
1. 确认 GitHub 仓库有代码
2. 查看 Vercel 部署日志
3. 重新部署

---

## 🎉 完成！

恭喜你！现在你拥有了一个全新的、漂亮的网站，包括：

✅ **动态渐变背景** - 浮动的彩色球体
✅ **粒子效果** - 漂浮的白色小粒子
✅ **玻璃态设计** - 毛玻璃卡片效果
✅ **现代化配色** - 紫蓝粉渐变主题
✅ **响应式布局** - 完美适配所有设备
✅ **企业级安全** - SHA-256 加密、会话管理
✅ **完整管理后台** - 登录、管理界面

---

## 📞 需要帮助？

如果遇到任何问题：
1. 把错误信息复制下来
2. 告诉我具体在哪一步
3. 我会帮你解决

---

## 📊 预计总耗时

| 步骤 | 耗时 |
|------|------|
| 获取 GitHub Token | 2 分钟 |
| 编辑部署脚本 | 1 分钟 |
| 运行部署脚本 | 1 分钟 |
| Vercel 部署 | 2 分钟 |
| 绑定域名（可选） | 10 分钟 |
| **总计** | **5-15 分钟** |

---

## 🚀 现在就开始吧！

**第一步：获取 GitHub Token**
访问：https://github.com/settings/tokens

**第二步：编辑脚本**
```bash
nano mac_deploy.sh
```

**第三步：运行脚本**
```bash
bash mac_deploy.sh
```

**第四步：Vercel 部署**
访问：https://vercel.com

**祝部署顺利！** 🎊
