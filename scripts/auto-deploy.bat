@echo off
REM 国文汇通 - 一键自动化部署脚本（Windows版本）
REM 适用于纯小白

echo ========================================
echo   🚀 国文汇通 - 一键部署脚本
echo ========================================
echo.

REM 设置颜色
set GREEN=[92m
set YELLOW=[93m
set RED=[91m
set BLUE=[94m
set NC=[0m

echo %BLUE%ℹ️  这个脚本将自动完成以下操作：%NC%
echo    1. 检查环境（Node.js、Git、Vercel CLI）
echo    2. 初始化 Git 仓库
echo    3. 创建 GitHub 仓库
echo    4. 推送代码到 GitHub
echo    5. 登录 Vercel
echo    6. 部署到 Vercel
echo.

set /p continue="是否继续？(y/n): "
if /i not "%continue%"=="y" (
    echo %YELLOW%部署已取消%NC%
    pause
    exit /b 0
)

echo.
echo %GREEN%========== 开始部署 ==========%NC%
echo.

REM 检查 Node.js
echo %BLUE%========== 检查 Node.js ==========%NC%
where node >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('node -v') do set NODE_VERSION=%%i
    echo %GREEN%✅ Node.js 已安装: %NODE_VERSION%%NC%
) else (
    echo %RED%❌ Node.js 未安装%NC%
    echo %YELLOW%请访问 https://nodejs.org/ 下载并安装 Node.js%NC%
    echo %YELLOW%安装完成后重新运行此脚本%NC%
    pause
    exit /b 1
)
echo.

REM 检查 Git
echo %BLUE%========== 检查 Git ==========%NC%
where git >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('git --version') do set GIT_VERSION=%%i
    echo %GREEN%✅ Git 已安装: %GIT_VERSION%%NC%
) else (
    echo %RED%❌ Git 未安装%NC%
    echo %YELLOW%请访问 https://git-scm.com/ 下载并安装 Git%NC%
    echo %YELLOW%安装完成后重新运行此脚本%NC%
    pause
    exit /b 1
)
echo.

REM 检查 Vercel CLI
echo %BLUE%========== 检查 Vercel CLI ==========%NC%
where vercel >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('vercel --version') do set VERCEL_VERSION=%%i
    echo %GREEN%✅ Vercel CLI 已安装: %VERCEL_VERSION%%NC%
) else (
    echo %YELLOW%⚠️  Vercel CLI 未安装%NC%
    echo %BLUE%正在安装 Vercel CLI...%NC%
    call npm install -g vercel
    echo %GREEN%✅ Vercel CLI 安装完成%NC%
)
echo.

REM 检查项目文件
echo %BLUE%========== 检查项目文件 ==========%NC%
if exist "assets" (
    echo %GREEN%✅ assets 文件夹存在%NC%
    
    if exist "assets\index.html" (
        echo %GREEN%✅ index.html 存在%NC%
    ) else (
        echo %RED%❌ index.html 不存在%NC%
        pause
        exit /b 1
    )
    
    if exist "assets\admin.html" (
        echo %GREEN%✅ admin.html 存在%NC%
    ) else (
        echo %RED%❌ admin.html 不存在%NC%
        pause
        exit /b 1
    )
) else (
    echo %RED%❌ assets 文件夹不存在%NC%
    pause
    exit /b 1
)
echo.

REM 初始化 Git 仓库
echo %BLUE%========== 初始化 Git 仓库 ==========%NC%
if exist ".git" (
    echo %YELLOW%⚠️  Git 仓库已存在%NC%
    set /p reinit="是否重新初始化？(y/n): "
    if /i "%reinit%"=="y" (
        rmdir /s /q .git
        git init
        echo %GREEN%✅ Git 仓库重新初始化%NC%
    )
) else (
    git init
    echo %GREEN%✅ Git 仓库初始化%NC%
)
echo.

REM 添加文件到 Git
echo %BLUE%========== 添加文件到 Git ==========%NC%
git add assets\
echo %GREEN%✅ 文件已添加%NC%
echo.

REM 提交文件
echo %BLUE%========== 提交文件 ==========%NC%
git commit -m "Initial commit: 部署国文汇通资料管理系统"
echo %GREEN%✅ 文件已提交%NC%
echo.

REM 创建 GitHub 仓库
echo %BLUE%========== 创建 GitHub 仓库 ==========%NC%
echo %BLUE%请按照以下步骤创建 GitHub 仓库：%NC%
echo.
echo 1. 访问: https://github.com/new
echo 2. 填写仓库信息:
echo    - Repository name: guowen-huitong-docs
echo    - Description: 国文汇通 - 专业的资料管理系统
echo    - 选择: Public（公开）
echo 3. 点击 "Create repository"
echo.

set /p repo_created="完成了吗？按 Enter 继续..."

echo.
echo %BLUE%请输入你的 GitHub 用户名:%NC%
set /p GITHUB_USERNAME=

set GIT_REPO_URL=https://github.com/%GITHUB_USERNAME%/guowen-huitong-docs.git
echo %BLUE%Git 仓库地址: %GIT_REPO_URL%%NC%
echo.

REM 关联远程仓库
echo %BLUE%========== 关联远程仓库 ==========%NC%
git remote get-url origin >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo %YELLOW%⚠️  远程仓库已存在%NC%
    git remote set-url origin %GIT_REPO_URL%
    echo %GREEN%✅ 远程仓库已更新%NC%
) else (
    git remote add origin %GIT_REPO_URL%
    echo %GREEN%✅ 远程仓库已关联%NC%
)
echo.

REM 推送到 GitHub
echo %BLUE%========== 推送到 GitHub ==========%NC%
echo %BLUE%正在推送文件...%NC%
git push -u origin main
if %ERRORLEVEL% NEQ 0 (
    echo %YELLOW%尝试使用 master 分支...%NC%
    git push -u origin master
)
echo %GREEN%✅ 文件已推送到 GitHub%NC%
echo %BLUE%仓库地址: %GIT_REPO_URL%%NC%
echo.

REM 登录 Vercel
echo %BLUE%========== 登录 Vercel ==========%NC%
echo %BLUE%将会打开浏览器进行登录...%NC%
vercel login
echo %GREEN%✅ Vercel 登录成功%NC%
echo.

REM 部署到 Vercel
echo %BLUE%========== 部署到 Vercel ==========%NC%
echo %BLUE%正在部署...%NC%

cd assets
vercel
cd ..

echo %GREEN%✅ 部署完成！%NC%
echo.

REM 生产环境部署
set /p prod="是否部署到生产环境？(y/n): "
if /i "%prod%"=="y" (
    echo %BLUE%========== 部署到生产环境 ==========%NC%
    cd assets
    vercel --prod
    cd ..
    echo %GREEN%✅ 生产环境部署完成！%NC%
    echo.
)

REM 显示完成信息
echo ========================================
echo   🎉 部署完成！
echo ========================================
echo.
echo %BLUE%📱 访问地址：%NC%
echo    https://guowen-huitong-docs.vercel.app
echo    https://guowen-huitong-docs.vercel.app/admin
echo.
echo %BLUE%🔗 GitHub 仓库：%NC%
echo    %GIT_REPO_URL%
echo.
echo %BLUE%📖 下一步：%NC%
echo    1. 访问你的网站
echo    2. 查看管理后台
echo    3. 绑定自定义域名（可选）
echo    4. 提交到搜索引擎（可选）
echo.
echo %BLUE%💡 提示：%NC%
echo    - 绑定域名：查看 QUICK_START.md
echo    - SEO 优化：查看 QUICK_START.md
echo    - 常见问题：查看 DEPLOY.md
echo.
echo ========================================

pause
