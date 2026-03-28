#!/bin/bash

################################################################################
# 国文汇通 - 全自动管理脚本
# 功能：启动/停止/重启/部署 网站
################################################################################

# 配置
PROJECT_DIR="/workspace/projects"
PORT=8000
LOG_FILE="/app/work/logs/bypass/app.log"
GITHUB_REPO="https://github.com/yitai121/guowen-huitong-docs"
VERCEL_PROJECT="guowen-huitong-docs"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 函数定义

print_header() {
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}           ${GREEN}🚀 国文汇通 - 全自动管理系统${NC}             ${CYAN}║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_server_status() {
    if ps aux | grep "http.server" | grep -v grep | grep -q ":$PORT"; then
        echo "running"
    else
        echo "stopped"
    fi
}

start_server() {
    print_header
    print_info "正在启动本地服务器..."

    local status=$(check_server_status)
    if [ "$status" == "running" ]; then
        print_info "服务器已经在运行中"
    else
        cd $PROJECT_DIR
        nohup python3 -m http.server $PORT > $LOG_FILE 2>&1 &
        sleep 2

        if [ "$(check_server_status)" == "running" ]; then
            print_success "服务器启动成功！"
            print_info "访问地址: ${GREEN}http://localhost:$PORT${NC}"
        else
            print_error "服务器启动失败"
            return 1
        fi
    fi
}

stop_server() {
    print_header
    print_info "正在停止本地服务器..."

    local status=$(check_server_status)
    if [ "$status" == "stopped" ]; then
        print_info "服务器已经停止"
    else
        pkill -f "http.server"
        sleep 1

        if [ "$(check_server_status)" == "stopped" ]; then
            print_success "服务器已停止"
        else
            print_error "服务器停止失败"
            return 1
        fi
    fi
}

restart_server() {
    print_header
    print_info "正在重启本地服务器..."
    stop_server
    start_server
}

status() {
    print_header

    print_info "系统状态检查："
    echo ""

    # 服务器状态
    local server_status=$(check_server_status)
    echo -e "本地服务器: ${GREEN}${server_status}${NC}"

    if [ "$server_status" == "running" ]; then
        echo -e "访问地址: ${GREEN}http://localhost:$PORT${NC}"
        echo -e "日志文件: ${GREEN}$LOG_FILE${NC}"
    fi

    echo ""

    # 文件检查
    print_info "文件检查："

    if [ -f "$PROJECT_DIR/index.html" ]; then
        echo -e "  ${GREEN}✓${NC} index.html 存在"
    else
        echo -e "  ${RED}✗${NC} index.html 不存在"
    fi

    if [ -f "$PROJECT_DIR/admin.html" ]; then
        echo -e "  ${GREEN}✓${NC} admin.html 存在"
    else
        echo -e "  ${RED}✗${NC} admin.html 不存在"
    fi

    if [ -f "$PROJECT_DIR/vercel.json" ]; then
        echo -e "  ${GREEN}✓${NC} vercel.json 存在"
    else
        echo -e "  ${RED}✗${NC} vercel.json 不存在"
    fi

    echo ""

    # Git 状态
    print_info "Git 状态："
    if [ -d "$PROJECT_DIR/.git" ]; then
        echo -e "  ${GREEN}✓${NC} Git 仓库已初始化"
    else
        echo -e "  ${RED}✗${NC} Git 仓库未初始化"
    fi
}

deploy_local() {
    print_header
    print_info "部署到本地..."

    start_server

    print_success "本地部署完成！"
    print_info "访问地址: ${GREEN}http://localhost:$PORT${NC}"
}

deploy_github() {
    print_header
    print_info "部署到 GitHub..."

    cd $PROJECT_DIR

    print_info "检查 Git 仓库..."
    if [ ! -d ".git" ]; then
        print_info "初始化 Git 仓库..."
        git init
        git config user.name "yitai121"
        git config user.email "862847146@qq.com"
    fi

    print_info "添加文件..."
    git add .

    print_info "提交更改..."
    git commit -m "update: 更新网站内容

更新时间: $(date '+%Y-%m-%d %H:%M:%S')"

    print_info "推送到 GitHub..."
    git push origin main

    print_success "GitHub 部署完成！"
    print_info "仓库地址: ${GREEN}$GITHUB_REPO${NC}"
}

show_logs() {
    print_header
    print_info "最近 20 行日志："
    echo ""
    tail -n 20 $LOG_FILE 2>/dev/null || echo "日志文件不存在"
}

show_help() {
    print_header
    echo "使用方法："
    echo ""
    echo "  $0 start       - 启动本地服务器"
    echo "  $0 stop        - 停止本地服务器"
    echo "  $0 restart     - 重启本地服务器"
    echo "  $0 status      - 查看系统状态"
    echo "  $0 deploy      - 部署到本地"
    echo "  $0 github      - 部署到 GitHub"
    echo "  $0 logs        - 查看日志"
    echo "  $0 help        - 显示帮助信息"
    echo ""
    echo "访问地址："
    echo "  本地: http://localhost:$PORT"
    echo "  GitHub: $GITHUB_REPO"
    echo "  Vercel: https://$VERCEL_PROJECT.vercel.app"
}

# 主流程

case "$1" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        restart_server
        ;;
    status)
        status
        ;;
    deploy)
        deploy_local
        ;;
    github)
        deploy_github
        ;;
    logs)
        show_logs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_header
        echo -e "${YELLOW}未指定命令，显示系统状态...${NC}"
        status
        echo ""
        show_help
        ;;
esac
