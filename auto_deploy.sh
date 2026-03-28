#!/bin/bash

################################################################################
# 国文汇通 - 全自动部署脚本
# 使用方法：
# 1. 修改下面的配置信息（GitHub用户名、仓库、token等）
# 2. 运行脚本：bash auto_deploy.sh
################################################################################

# ========================================
# 🔐 第一步：填入你的配置信息
# ========================================

# GitHub 配置
GITHUB_USERNAME=""           # 你的 GitHub 用户名
GITHUB_REPO_NAME="guowen-huitong-docs"  # 仓库名称（可以不改）
GITHUB_EMAIL=""              # 你的 GitHub 邮箱
GITHUB_TOKEN=""              # GitHub Personal Access Token

# Git 配置
GIT_NAME=""                  # 你的名字（用于 git commit）

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ========================================
# 函数定义
# ========================================

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_config() {
    print_info "检查配置信息..."

    if [ -z "$GITHUB_USERNAME" ]; then
        print_error "请填写 GITHUB_USERNAME"
        exit 1
    fi

    if [ -z "$GITHUB_EMAIL" ]; then
        print_error "请填写 GITHUB_EMAIL"
        exit 1
    fi

    if [ -z "$GITHUB_TOKEN" ]; then
        print_error "请填写 GITHUB_TOKEN"
        echo ""
        echo "📖 如何获取 GitHub Token："
        echo "   1. 访问: https://github.com/settings/tokens"
        echo "   2. 点击 'Generate new token' -> 'Generate new token (classic)'"
        echo "   3. 勾选 'repo' 权限"
        echo "   4. 点击生成，复制 token"
        exit 1
    fi

    if [ -z "$GIT_NAME" ]; then
        print_error "请填写 GIT_NAME"
        exit 1
    fi

    print_success "配置信息检查通过"
}

init_git() {
    print_info "初始化 Git 仓库..."

    if [ -d ".git" ]; then
        print_warning "Git 仓库已存在，跳过初始化"
    else
        git init
        print_success "Git 仓库初始化完成"
    fi
}

config_git() {
    print_info "配置 Git 用户信息..."

    git config user.name "$GIT_NAME"
    git config user.email "$GITHUB_EMAIL"

    print_success "Git 配置完成"
}

add_files() {
    print_info "添加所有文件..."

    git add .

    print_success "文件添加完成"
}

commit_files() {
    print_info "提交代码..."

    git commit -m "feat: 全面UI重构 - 互联网大厂级视觉设计

核心更新：
- 重构主页 - 动态渐变背景、粒子效果、玻璃态设计
- 新增管理员登录页 - 现代化登录界面
- 新增管理后台 - 统一视觉风格
- 新增安全配置库 - SHA-256加密、会话管理
- 修复路由配置 - 解决/admin 404问题"

    print_success "代码提交完成"
}

create_github_repo() {
    print_info "创建 GitHub 仓库..."

    # 检查仓库是否已存在
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/$GITHUB_USERNAME/$GITHUB_REPO_NAME")

    if [ "$RESPONSE" = "200" ]; then
        print_warning "仓库已存在，跳过创建"
    else
        # 创建新仓库
        curl -s -X POST \
            -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/user/repos" \
            -d "{
                \"name\": \"$GITHUB_REPO_NAME\",
                \"description\": \"国文汇通 - 企业知识管理平台\",
                \"private\": false,
                \"auto_init\": false
            }" > /dev/null

        if [ $? -eq 0 ]; then
            print_success "GitHub 仓库创建成功"
        else
            print_error "GitHub 仓库创建失败"
            exit 1
        fi
    fi
}

add_remote() {
    print_info "添加远程仓库..."

    git remote remove origin 2>/dev/null
    git remote add origin "https://$GITHUB_TOKEN@github.com/$GITHUB_USERNAME/$GITHUB_REPO_NAME.git"

    print_success "远程仓库添加完成"
}

push_code() {
    print_info "推送代码到 GitHub..."

    git branch -M main

    git push -u origin main

    if [ $? -eq 0 ]; then
        print_success "代码推送成功！"
    else
        print_error "代码推送失败，请检查网络和 token"
        exit 1
    fi
}

print_next_steps() {
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🎉 自动部署第一步完成！${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BLUE}📦 你的 GitHub 仓库地址：${NC}"
    echo "   https://github.com/$GITHUB_USERNAME/$GITHUB_REPO_NAME"
    echo ""
    echo -e "${YELLOW}🚀 接下来需要你在 Vercel 手动操作（3分钟）：${NC}"
    echo ""
    echo "   1. 访问 Vercel: https://vercel.com"
    echo "   2. 点击 'Add New Project'"
    echo "   3. 导入仓库: $GITHUB_REPO_NAME"
    echo "   4. 点击 'Deploy' 按钮"
    echo "   5. 等待部署完成（1-2分钟）"
    echo ""
    echo -e "${BLUE}🌐 部署完成后访问：${NC}"
    echo "   https://$GITHUB_REPO_NAME.vercel.app"
    echo ""
    echo -e "${YELLOW}📖 绑定域名（可选）：${NC}"
    echo "   1. 在 Vercel 项目设置中添加域名: www.guowenhuitong.com"
    echo "   2. 配置 DNS 记录"
    echo "   3. 等待 DNS 生效"
    echo ""
    echo -e "${GREEN}✅ 需要帮助？查看 '纯小白部署指南.md'${NC}"
    echo ""
}

# ========================================
# 主流程
# ========================================

main() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}🚀 国文汇通 - 自动化部署脚本${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo ""

    # 检查配置
    check_config

    # 初始化 Git
    init_git

    # 配置 Git
    config_git

    # 添加文件
    add_files

    # 提交文件
    commit_files

    # 创建 GitHub 仓库
    create_github_repo

    # 添加远程仓库
    add_remote

    # 推送代码
    push_code

    # 打印下一步操作
    print_next_steps
}

# 运行主流程
main
