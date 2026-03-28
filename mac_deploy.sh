#!/bin/bash

################################################################################
# 国文汇通 - Mac M 芯片专属部署脚本
# 使用方法：
# 1. 修改下面的配置信息（GitHub用户名、仓库、token等）
# 2. 运行脚本：bash mac_deploy.sh
################################################################################

# ========================================
# 🔐 第一步：填入你的配置信息
# ========================================

# GitHub 配置
GITHUB_USERNAME="yitai121"           # 你的 GitHub 用户名
GITHUB_REPO_NAME="guowen-huitong-docs"  # 仓库名称（可以不改）
GITHUB_EMAIL="862847146@qq.com"              # 你的 GitHub 邮箱
GITHUB_TOKEN=""              # GitHub Personal Access Token (通过环境变量 GITHUB_TOKEN 设置)

# Git 配置
GIT_NAME="yitai64"                  # 你的名字（用于 git commit）

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ========================================
# 函数定义
# ========================================

print_header() {
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}           ${GREEN}🚀 国文汇通 - Mac M 芯片自动化部署${NC}            ${CYAN}║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

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

print_step() {
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

check_config() {
    print_step "检查配置信息"

    if [ -z "$GITHUB_USERNAME" ]; then
        print_error "请填写 GITHUB_USERNAME"
        echo ""
        echo "📖 编辑脚本的方法："
        echo "   nano mac_deploy.sh"
        echo "   # 填写信息后："
        echo "   # Ctrl+O 保存"
        echo "   # Ctrl+X 退出"
        echo ""
        exit 1
    fi

    if [ -z "$GITHUB_EMAIL" ]; then
        print_error "请填写 GITHUB_EMAIL"
        echo ""
        echo "📖 编辑脚本的方法："
        echo "   nano mac_deploy.sh"
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
        echo ""
        exit 1
    fi

    if [ -z "$GIT_NAME" ]; then
        print_error "请填写 GIT_NAME"
        echo ""
        echo "📖 编辑脚本的方法："
        echo "   nano mac_deploy.sh"
        exit 1
    fi

    print_success "配置信息检查通过"
    echo ""
    echo -e "${BLUE}配置信息预览：${NC}"
    echo "  GitHub 用户名: ${GREEN}$GITHUB_USERNAME${NC}"
    echo "  GitHub 邮箱:   ${GREEN}$GITHUB_EMAIL${NC}"
    echo "  仓库名称:      ${GREEN}$GITHUB_REPO_NAME${NC}"
    echo "  你的名字:      ${GREEN}$GIT_NAME${NC}"
    echo "  Token:         ${GREEN}${GITHUB_TOKEN:0:10}...${NC} (已脱敏)"
    echo ""
}

check_git() {
    print_step "检查 Git 环境"

    if ! command -v git &> /dev/null; then
        print_error "Git 未安装"
        echo ""
        echo "📖 如何安装 Git："
        echo "   Mac 已预装 Git，如果没有，请运行："
        echo "   xcode-select --install"
        echo ""
        exit 1
    fi

    git_version=$(git --version)
    print_success "Git 已安装: $git_version"
    echo ""
}

init_git() {
    print_step "初始化 Git 仓库"

    if [ -d ".git" ]; then
        print_warning "Git 仓库已存在，将重新配置"
    else
        git init
        print_success "Git 仓库初始化完成"
    fi
    echo ""
}

config_git() {
    print_step "配置 Git 用户信息"

    git config user.name "$GIT_NAME"
    git config user.email "$GITHUB_EMAIL"

    print_success "Git 配置完成"
    echo ""
}

add_files() {
    print_step "添加所有文件"

    git add .

    # 统计添加的文件数
    file_count=$(git diff --cached --name-only | wc -l | tr -d ' ')

    print_success "已添加 $file_count 个文件到暂存区"
    echo ""
}

commit_files() {
    print_step "提交代码"

    git commit -m "feat: 全面UI重构 - 互联网大厂级视觉设计

核心更新：
- 重构主页 - 动态渐变背景、粒子效果、玻璃态设计
- 新增管理员登录页 - 现代化登录界面
- 新增管理后台 - 统一视觉风格
- 新增安全配置库 - SHA-256加密、会话管理
- 修复路由配置 - 解决/admin 404问题
- 新增自动化部署脚本 - 支持 Mac/Windows/Linux"

    print_success "代码提交完成"
    echo ""
}

create_github_repo() {
    print_step "创建 GitHub 仓库"

    # 检查仓库是否已存在
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/$GITHUB_USERNAME/$GITHUB_REPO_NAME")

    if [ "$RESPONSE" = "200" ]; then
        print_warning "仓库已存在: $GITHUB_REPO_NAME"
        echo "  仓库地址: https://github.com/$GITHUB_USERNAME/$GITHUB_REPO_NAME"
    else
        print_info "正在创建新仓库: $GITHUB_REPO_NAME"

        # 创建新仓库
        CREATE_RESPONSE=$(curl -s -X POST \
            -H "Authorization: token $GITHUB_TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/user/repos" \
            -d "{
                \"name\": \"$GITHUB_REPO_NAME\",
                \"description\": \"国文汇通 - 企业知识管理平台\",
                \"private\": false,
                \"auto_init\": false
            }")

        if echo "$CREATE_RESPONSE" | grep -q "html_url"; then
            print_success "GitHub 仓库创建成功"
            REPO_URL=$(echo "$CREATE_RESPONSE" | grep -o '"html_url":"[^"]*' | cut -d'"' -f4)
            echo "  仓库地址: $REPO_URL"
        else
            print_error "GitHub 仓库创建失败"
            echo ""
            echo "错误信息:"
            echo "$CREATE_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$CREATE_RESPONSE"
            exit 1
        fi
    fi
    echo ""
}

add_remote() {
    print_step "配置远程仓库"

    git remote remove origin 2>/dev/null
    git remote add origin "https://$GITHUB_TOKEN@github.com/$GITHUB_USERNAME/$GITHUB_REPO_NAME.git"

    print_success "远程仓库配置完成"
    echo ""
}

push_code() {
    print_step "推送代码到 GitHub"

    git branch -M main

    echo -e "${BLUE}正在推送代码...${NC}"
    git push -u origin main

    if [ $? -eq 0 ]; then
        print_success "代码推送成功！"
        echo ""
        echo -e "${GREEN}🎉 GitHub 仓库地址：${NC}"
        echo "   https://github.com/$GITHUB_USERNAME/$GITHUB_REPO_NAME"
    else
        print_error "代码推送失败"
        echo ""
        echo "可能的原因："
        echo "  1. 网络连接问题"
        echo "  2. GitHub Token 无效或已过期"
        echo "  3. 仓库名称冲突"
        echo ""
        echo "解决方法："
        echo "  1. 检查网络连接"
        echo "  2. 重新生成 GitHub Token"
        echo "  3. 确认仓库名称是否正确"
        exit 1
    fi
    echo ""
}

print_next_steps() {
    print_step "下一步操作"

    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🎉 自动部署第一步完成！${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}📦 你的 GitHub 仓库：${NC}"
    echo "   https://github.com/$GITHUB_USERNAME/$GITHUB_REPO_NAME"
    echo ""
    echo -e "${YELLOW}🚀 接下来在 Vercel 部署（3分钟）：${NC}"
    echo ""
    echo "   1. 打开浏览器访问: ${GREEN}https://vercel.com${NC}"
    echo "   2. 用 GitHub 账号登录"
    echo "   3. 点击 'Add New Project'"
    echo "   4. 找到并导入仓库: ${GREEN}$GITHUB_REPO_NAME${NC}"
    echo "   5. 点击 'Deploy' 按钮"
    echo "   6. 等待部署完成（1-2分钟）"
    echo ""
    echo -e "${CYAN}🌐 部署完成后访问：${NC}"
    echo "   ${GREEN}https://$GITHUB_REPO_NAME.vercel.app${NC}"
    echo ""
    echo -e "${YELLOW}📖 绑定自定义域名 www.guowenhuitong.com（可选）：${NC}"
    echo ""
    echo "   1. 在 Vercel 项目设置中点击 'Domains'"
    echo "   2. 添加域名: ${GREEN}www.guowenhuitong.com${NC}"
    echo "   3. 选择 'Use Vercel DNS'（推荐）"
    echo "   4. 等待 DNS 生效（10-30分钟）"
    echo ""
    echo -e "${CYAN}🔐 管理员登录信息：${NC}"
    echo "   登录地址: ${GREEN}https://www.guowenhuitong.com/admin/login.html${NC}"
    echo "   用户名: ${GREEN}admin${NC}"
    echo "   密码: ${GREEN}admin888${NC}"
    echo ""
    echo -e "${GREEN}✅ 需要帮助？${NC}"
    echo "   查看详细指南: ${GREEN}Mac_M芯片部署指南.md${NC}"
    echo ""
}

# ========================================
# 主流程
# ========================================

main() {
    print_header

    # 检查配置
    check_config

    # 检查 Git
    check_git

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
