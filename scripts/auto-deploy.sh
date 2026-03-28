#!/bin/bash

#############################################
# 国文汇通 - 一键自动化部署脚本
# 适用于纯小白
#############################################

set -e  # 遇到错误立即退出

echo "========================================"
echo "  🚀 国文汇通 - 一键部署脚本"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_step() {
    echo ""
    echo -e "${GREEN}========== $1 ==========${NC}"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查 Node.js
check_nodejs() {
    print_step "检查 Node.js"
    
    if command_exists node; then
        NODE_VERSION=$(node -v)
        print_success "Node.js 已安装: $NODE_VERSION"
    else
        print_error "Node.js 未安装"
        print_info "正在下载 Node.js..."
        
        # 下载 Node.js
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command_exists brew; then
                brew install node
            else
                print_error "请先安装 Homebrew: https://brew.sh/"
                exit 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
            sudo apt-get install -y nodejs
        else
            # Windows
            print_error "Windows 用户请手动安装 Node.js: https://nodejs.org/"
            exit 1
        fi
        
        print_success "Node.js 安装完成"
    fi
    
    echo ""
}

# 检查 Git
check_git() {
    print_step "检查 Git"
    
    if command_exists git; then
        GIT_VERSION=$(git --version)
        print_success "Git 已安装: $GIT_VERSION"
    else
        print_error "Git 未安装"
        print_info "正在安装 Git..."
        
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command_exists brew; then
                brew install git
            else
                print_error "请先安装 Homebrew: https://brew.sh/"
                exit 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            sudo apt-get update
            sudo apt-get install -y git
        else
            # Windows
            print_error "Windows 用户请手动安装 Git: https://git-scm.com/"
            exit 1
        fi
        
        print_success "Git 安装完成"
    fi
    
    echo ""
}

# 检查 Vercel CLI
check_vercel() {
    print_step "检查 Vercel CLI"
    
    if command_exists vercel; then
        VERCEL_VERSION=$(vercel --version)
        print_success "Vercel CLI 已安装: $VERCEL_VERSION"
    else
        print_warning "Vercel CLI 未安装"
        print_info "正在安装 Vercel CLI..."
        
        npm install -g vercel
        
        print_success "Vercel CLI 安装完成"
    fi
    
    echo ""
}

# 检查 GitHub
check_github() {
    print_step "检查 GitHub 配置"
    
    if git config --global user.name >/dev/null 2>&1; then
        GIT_USER=$(git config --global user.name)
        print_success "GitHub 用户名已配置: $GIT_USER"
    else
        print_warning "GitHub 用户名未配置"
        print_info "请输入你的 GitHub 用户名:"
        read -p "> " GITHUB_USERNAME
        
        git config --global user.name "$GITHUB_USERNAME"
        git config --global user.email "$GITHUB_USERNAME@users.noreply.github.com"
        
        print_success "GitHub 配置完成"
    fi
    
    echo ""
}

# 检查项目文件
check_files() {
    print_step "检查项目文件"
    
    if [ -d "assets" ]; then
        print_success "assets 文件夹存在"
        
        # 检查必要文件
        if [ -f "assets/index.html" ]; then
            print_success "index.html 存在"
        else
            print_error "index.html 不存在"
            exit 1
        fi
        
        if [ -f "assets/admin.html" ]; then
            print_success "admin.html 存在"
        else
            print_error "admin.html 不存在"
            exit 1
        fi
        
        if [ -f "assets/guowen_huitong_data.json" ]; then
            print_success "guowen_huitong_data.json 存在"
        else
            print_warning "guowen_huitong_data.json 不存在，将使用默认数据"
        fi
    else
        print_error "assets 文件夹不存在"
        exit 1
    fi
    
    echo ""
}

# 初始化 Git 仓库
init_git() {
    print_step "初始化 Git 仓库"
    
    if [ -d ".git" ]; then
        print_warning "Git 仓库已存在"
        read -p "是否重新初始化？(y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf .git
            git init
            print_success "Git 仓库重新初始化"
        fi
    else
        git init
        print_success "Git 仓库初始化"
    fi
    
    echo ""
}

# 添加文件到 Git
add_files() {
    print_step "添加文件到 Git"
    
    git add assets/
    print_success "文件已添加"
    
    echo ""
}

# 提交文件
commit_files() {
    print_step "提交文件"
    
    git commit -m "Initial commit: 部署国文汇通资料管理系统"
    print_success "文件已提交"
    
    echo ""
}

# 创建 GitHub 仓库（需要手动操作）
create_github_repo() {
    print_step "创建 GitHub 仓库"
    
    print_info "请按照以下步骤创建 GitHub 仓库："
    echo ""
    echo "1. 访问: https://github.com/new"
    echo "2. 填写仓库信息:"
    echo "   - Repository name: guowen-huitong-docs"
    echo "   - Description: 国文汇通 - 专业的资料管理系统"
    echo "   - 选择: Public（公开）"
    echo "3. 点击 'Create repository'"
    echo ""
    
    read -p "完成了吗？按 Enter 继续..."
    
    print_info "请输入你的 GitHub 用户名:"
    read -p "> " GITHUB_USERNAME
    
    GIT_REPO_URL="https://github.com/${GITHUB_USERNAME}/guowen-huitong-docs.git"
    
    print_info "Git 仓库地址: $GIT_REPO_URL"
    
    echo ""
}

# 关联远程仓库
link_remote() {
    print_step "关联远程仓库"
    
    if [ -z "$GIT_REPO_URL" ]; then
        print_error "Git 仓库地址未设置"
        exit 1
    fi
    
    if git remote get-url origin >/dev/null 2>&1; then
        print_warning "远程仓库已存在"
        git remote set-url origin "$GIT_REPO_URL"
        print_success "远程仓库已更新"
    else
        git remote add origin "$GIT_REPO_URL"
        print_success "远程仓库已关联"
    fi
    
    echo ""
}

# 推送到 GitHub
push_to_github() {
    print_step "推送到 GitHub"
    
    print_info "正在推送文件..."
    git push -u origin main || git push -u origin master
    
    print_success "文件已推送到 GitHub"
    print_info "仓库地址: $GIT_REPO_URL"
    
    echo ""
}

# 登录 Vercel
login_vercel() {
    print_step "登录 Vercel"
    
    print_info "将会打开浏览器进行登录..."
    vercel login
    
    print_success "Vercel 登录成功"
    
    echo ""
}

# 部署到 Vercel
deploy_vercel() {
    print_step "部署到 Vercel"
    
    print_info "正在部署..."
    
    # 切换到 assets 目录
    cd assets
    
    # 部署
    vercel
    
    print_success "部署完成！"
    
    # 切回根目录
    cd ..
    
    echo ""
}

# 生产环境部署
deploy_production() {
    print_step "部署到生产环境"
    
    cd assets
    vercel --prod
    cd ..
    
    print_success "生产环境部署完成！"
    
    echo ""
}

# 显示完成信息
show_complete() {
    print_step "🎉 部署完成！"
    
    echo ""
    echo "=========================================="
    echo "  ✅ 你的网站已成功部署！"
    echo "=========================================="
    echo ""
    print_info "📱 访问地址："
    echo "   https://guowen-huitong-docs.vercel.app"
    echo "   https://guowen-huitong-docs.vercel.app/admin"
    echo ""
    print_info "🔗 GitHub 仓库："
    echo "   $GIT_REPO_URL"
    echo ""
    print_info "📖 下一步："
    echo "   1. 访问你的网站"
    echo "   2. 查看管理后台"
    echo "   3. 绑定自定义域名（可选）"
    echo "   4. 提交到搜索引擎（可选）"
    echo ""
    print_info "💡 提示："
    echo "   - 绑定域名：查看 QUICK_START.md"
    echo "   - SEO 优化：查看 QUICK_START.md"
    echo "   - 常见问题：查看 DEPLOY.md"
    echo ""
    echo "=========================================="
}

# 主函数
main() {
    # 欢迎信息
    echo ""
    echo "🚀 国文汇通 - 一键部署脚本"
    echo ""
    print_info "这个脚本将自动完成以下操作："
    echo "   1. 检查环境（Node.js、Git、Vercel CLI）"
    echo "   2. 初始化 Git 仓库"
    echo "   3. 创建 GitHub 仓库"
    echo "   4. 推送代码到 GitHub"
    echo "   5. 登录 Vercel"
    echo "   6. 部署到 Vercel"
    echo ""
    
    read -p "是否继续？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "部署已取消"
        exit 0
    fi
    
    echo ""
    
    # 检查环境
    check_nodejs
    check_git
    check_vercel
    check_github
    check_files
    
    # Git 操作
    init_git
    add_files
    commit_files
    
    # 创建 GitHub 仓库
    create_github_repo
    
    # 推送到 GitHub
    link_remote
    push_to_github
    
    # 部署到 Vercel
    login_vercel
    deploy_vercel
    
    # 生产环境部署
    read -p "是否部署到生产环境？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        deploy_production
    fi
    
    # 显示完成信息
    show_complete
}

# 运行主函数
main

exit 0
