@echo off
REM ============================================================================
REM 国文汇通 - 全自动部署脚本 (Windows版)
REM 使用方法：
REM 1. 用记事本打开这个文件
REM 2. 修改下面的配置信息
REM 3. 双击运行这个脚本
REM ============================================================================

REM ========================================
REM 🔐 第一步：填入你的配置信息
REM ========================================

REM GitHub 配置
set GITHUB_USERNAME=
set GITHUB_REPO_NAME=guowen-huitong-docs
set GITHUB_EMAIL=
set GITHUB_TOKEN=

REM Git 配置
set GIT_NAME=

REM ========================================
REM 检查配置信息
REM ========================================

if "%GITHUB_USERNAME%"=="" (
    echo [错误] 请填写 GITHUB_USERNAME
    echo.
    echo 如何编辑：
    echo 1. 右键点击这个文件，选择"编辑"
    echo 2. 填写上面的配置信息
    echo 3. 保存并关闭
    echo 4. 重新双击运行
    pause
    exit /b 1
)

if "%GITHUB_EMAIL%"=="" (
    echo [错误] 请填写 GITHUB_EMAIL
    pause
    exit /b 1
)

if "%GITHUB_TOKEN%"=="" (
    echo [错误] 请填写 GITHUB_TOKEN
    echo.
    echo 如何获取 GitHub Token：
    echo 1. 访问: https://github.com/settings/tokens
    echo 2. 点击 "Generate new token" ^>^> "Generate new token (classic)"
    echo 3. 勾选 "repo" 权限
    echo 4. 点击生成，复制 token
    pause
    exit /b 1
)

if "%GIT_NAME%"=="" (
    echo [错误] 请填写 GIT_NAME
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🚀 国文汇通 - 自动化部署开始
echo ========================================
echo.

REM ========================================
REM 检查 Git 是否安装
REM ========================================

git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Git 未安装
    echo.
    echo 请先安装 Git：
    echo 1. 访问: https://git-scm.com/download/win
    echo 2. 下载并安装 Git
    echo 3. 安装完成后重新运行此脚本
    pause
    exit /b 1
)

echo [√] Git 已安装
echo.

REM ========================================
REM 初始化 Git 仓库
REM ========================================

echo [1/6] 初始化 Git 仓库...
if exist .git (
    echo [√] Git 仓库已存在，跳过初始化
) else (
    git init
    echo [√] Git 仓库初始化完成
)
echo.

REM ========================================
REM 配置 Git
REM ========================================

echo [2/6] 配置 Git 用户信息...
git config user.name "%GIT_NAME%"
git config user.email "%GITHUB_EMAIL%"
echo [√] Git 配置完成
echo.

REM ========================================
REM 添加文件
REM ========================================

echo [3/6] 添加所有文件...
git add .
echo [√] 文件添加完成
echo.

REM ========================================
REM 提交文件
REM ========================================

echo [4/6] 提交代码...
git commit -m "feat: 全面UI重构 - 互联网大厂级视觉设计"
echo [√] 代码提交完成
echo.

REM ========================================
REM 创建 GitHub 仓库
REM ========================================

echo [5/6] 创建 GitHub 仓库...

REM 检查仓库是否已存在（使用 curl）
curl -s -o nul -w "%%{http_code}" -H "Authorization: token %GITHUB_TOKEN%" "https://api.github.com/repos/%GITHUB_USERNAME%/%GITHUB_REPO_NAME%" > temp_http_code.txt
set /p HTTP_CODE=<temp_http_code.txt
del temp_http_code.txt

if "%HTTP_CODE%"=="200" (
    echo [√] 仓库已存在，跳过创建
) else (
    echo 正在创建新仓库...
    curl -s -X POST -H "Authorization: token %GITHUB_TOKEN%" -H "Accept: application/vnd.github.v3+json" -d "{\"name\":\"%GITHUB_REPO_NAME%\",\"description\":\"国文汇通 - 企业知识管理平台\",\"private\":false}" "https://api.github.com/user/repos"
    if errorlevel 1 (
        echo [错误] GitHub 仓库创建失败
        pause
        exit /b 1
    )
    echo [√] GitHub 仓库创建成功
)
echo.

REM ========================================
REM 添加远程仓库
REM ========================================

echo [6/6] 添加远程仓库...

git remote remove origin >nul 2>&1
git remote add origin https://%GITHUB_TOKEN%@github.com/%GITHUB_USERNAME%/%GITHUB_REPO_NAME%.git

echo [√] 远程仓库添加完成
echo.

REM ========================================
REM 推送代码
REM ========================================

echo [∏] 推送代码到 GitHub...

git branch -M main

git push -u origin main

if errorlevel 1 (
    echo [错误] 代码推送失败
    echo.
    echo 可能的原因：
    echo 1. 网络连接问题
    echo 2. GitHub Token 无效
    echo 3. 仓库名称冲突
    pause
    exit /b 1
)

echo [√] 代码推送成功！
echo.

REM ========================================
REM 打印下一步操作
REM ========================================

echo.
echo ========================================
echo 🎉 自动部署第一步完成！
echo ========================================
echo.
echo 📦 你的 GitHub 仓库地址：
echo    https://github.com/%GITHUB_USERNAME%/%GITHUB_REPO_NAME%
echo.
echo 🚀 接下来需要你在 Vercel 手动操作（3分钟）：
echo.
echo    1. 访问 Vercel: https://vercel.com
echo    2. 点击 "Add New Project"
echo    3. 导入仓库: %GITHUB_REPO_NAME%
echo    4. 点击 "Deploy" 按钮
echo    5. 等待部署完成（1-2分钟）
echo.
echo 🌐 部署完成后访问：
echo    https://%GITHUB_REPO_NAME%.vercel.app
echo.
echo 📖 绑定域名（可选）：
echo    1. 在 Vercel 项目设置中添加域名: www.guowenhuitong.com
echo    2. 配置 DNS 记录
echo    3. 等待 DNS 生效
echo.
echo ✅ 需要帮助？查看 "纯小白部署指南.md"
echo.

pause
