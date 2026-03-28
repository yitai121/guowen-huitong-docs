#!/bin/bash

################################################################################
# 国文汇通 - 小龙虾集群管理系统
# 功能：批量管理多个小龙虾实例
################################################################################

# 配置
CLUSTER_DIR="$HOME/guowen-huitong-cluster"
INSTANCES_FILE="$CLUSTER_DIR/instances.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# 函数定义

print_header() {
    clear
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}           ${GREEN}🤖 小龙虾集群管理系统${NC}                    ${CYAN}║${NC}"
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

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 初始化集群
init_cluster() {
    print_header
    print_info "初始化集群..."

    # 创建集群目录
    mkdir -p "$CLUSTER_DIR"

    # 创建实例配置文件
    if [ ! -f "$INSTANCES_FILE" ]; then
        echo '{"instances": []}' > "$INSTANCES_FILE"
        print_success "集群目录已创建"
    else
        print_info "集群已存在"
    fi

    print_info "集群目录: $CLUSTER_DIR"
}

# 添加实例
add_instance() {
    print_header
    print_info "添加新实例..."

    # 输入实例信息
    echo ""
    read -p "实例名称: " name
    read -p "端口 (默认8001): " port
    port=${port:-8001}
    read -p "描述 (可选): " description

    # 创建实例目录
    local instance_dir="$CLUSTER_DIR/$name"
    mkdir -p "$instance_dir"

    # 复制项目文件
    if [ -f "$SCRIPT_DIR/index.html" ]; then
        cp "$SCRIPT_DIR/index.html" "$instance_dir/"
        cp "$SCRIPT_DIR/admin.html" "$instance_dir/" 2>/dev/null || true
        cp "$SCRIPT_DIR/vercel.json" "$instance_dir/" 2>/dev/null || true
    fi

    # 创建管理脚本
    cat > "$instance_dir/manage.sh" << EOF
#!/bin/bash
PORT=$port
LOG_FILE="$instance_dir/app.log"
PID_FILE="$instance_dir/server.pid"

case "\$1" in
    start)
        python3 -m http.server \$PORT > \$LOG_FILE 2>&1 &
        echo \$! > \$PID_FILE
        echo "实例 $name 已启动，端口: \$PORT"
        ;;
    stop)
        if [ -f "\$PID_FILE" ]; then
            kill \$(cat \$PID_FILE) 2>/dev/null
            rm -f "\$PID_FILE"
            echo "实例 $name 已停止"
        fi
        ;;
    status)
        if [ -f "\$PID_FILE" ] && ps -p \$(cat \$PID_FILE) > /dev/null 2>&1; then
            echo "运行中 - 端口: \$PORT"
        else
            echo "已停止"
        fi
        ;;
    *)
        echo "用法: \$0 {start|stop|status}"
        ;;
esac
EOF

    chmod +x "$instance_dir/manage.sh"

    # 更新实例配置
    local config="$instance_dir/config.json"
    cat > "$config" << EOF
{
    "name": "$name",
    "port": $port,
    "description": "$description",
    "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "status": "stopped"
}
EOF

    print_success "实例 '$name' 已创建"
    print_info "端口: $port"
    print_info "目录: $instance_dir"

    list_instances
}

# 列出所有实例
list_instances() {
    print_header
    print_info "实例列表："
    echo ""

    if [ ! -d "$CLUSTER_DIR" ] || [ -z "$(ls -A $CLUSTER_DIR 2>/dev/null)" ]; then
        print_warning "没有找到任何实例"
        echo ""
        print_info "使用 'cluster.sh add' 添加新实例"
        return
    fi

    local count=0
    for instance_dir in "$CLUSTER_DIR"/*/; do
        if [ -d "$instance_dir" ]; then
            local name=$(basename "$instance_dir")
            local config="$instance_dir/config.json"

            if [ -f "$config" ]; then
                count=$((count + 1))
                echo -e "${CYAN}[$count] $name${NC}"

                # 读取配置
                local port=$(grep -o '"port":[^,]*' "$config" | cut -d: -f2)
                local description=$(grep -o '"description":"[^"]*"' "$config" | cut -d'"' -f4)
                local status="stopped"

                # 检查运行状态
                if [ -f "$instance_dir/server.pid" ]; then
                    local pid=$(cat "$instance_dir/server.pid")
                    if ps -p $pid > /dev/null 2>&1; then
                        status="${GREEN}running${NC}"
                    else
                        status="${RED}stopped${NC}"
                    fi
                fi

                echo "  端口: $port"
                echo "  状态: $status"
                echo "  描述: $description"
                echo ""
            fi
        fi
    done

    if [ $count -eq 0 ]; then
        print_warning "没有找到任何实例"
    fi
}

# 启动单个实例
start_instance() {
    local name=$1

    if [ -z "$name" ]; then
        print_error "请指定实例名称"
        return 1
    fi

    local instance_dir="$CLUSTER_DIR/$name"

    if [ ! -d "$instance_dir" ]; then
        print_error "实例 '$name' 不存在"
        return 1
    fi

    print_info "启动实例 '$name'..."
    cd "$instance_dir"
    ./manage.sh start

    if [ $? -eq 0 ]; then
        print_success "实例 '$name' 已启动"
    else
        print_error "实例 '$name' 启动失败"
    fi
}

# 停止单个实例
stop_instance() {
    local name=$1

    if [ -z "$name" ]; then
        print_error "请指定实例名称"
        return 1
    fi

    local instance_dir="$CLUSTER_DIR/$name"

    if [ ! -d "$instance_dir" ]; then
        print_error "实例 '$name' 不存在"
        return 1
    fi

    print_info "停止实例 '$name'..."
    cd "$instance_dir"
    ./manage.sh stop

    if [ $? -eq 0 ]; then
        print_success "实例 '$name' 已停止"
    else
        print_error "实例 '$name' 停止失败"
    fi
}

# 批量启动所有实例
start_all() {
    print_header
    print_info "批量启动所有实例..."
    echo ""

    if [ ! -d "$CLUSTER_DIR" ]; then
        print_error "集群目录不存在"
        return 1
    fi

    local count=0
    for instance_dir in "$CLUSTER_DIR"/*/; do
        if [ -d "$instance_dir" ]; then
            local name=$(basename "$instance_dir")
            print_info "启动实例: $name"

            cd "$instance_dir"
            ./manage.sh start > /dev/null 2>&1

            if [ $? -eq 0 ]; then
                print_success "✓ $name"
                count=$((count + 1))
            else
                print_error "✗ $name"
            fi
        fi
    done

    echo ""
    print_success "已启动 $count 个实例"
}

# 批量停止所有实例
stop_all() {
    print_header
    print_info "批量停止所有实例..."
    echo ""

    if [ ! -d "$CLUSTER_DIR" ]; then
        print_error "集群目录不存在"
        return 1
    fi

    local count=0
    for instance_dir in "$CLUSTER_DIR"/*/; do
        if [ -d "$instance_dir" ]; then
            local name=$(basename "$instance_dir")
            print_info "停止实例: $name"

            cd "$instance_dir"
            ./manage.sh stop > /dev/null 2>&1

            if [ $? -eq 0 ]; then
                print_success "✓ $name"
                count=$((count + 1))
            else
                print_error "✗ $name"
            fi
        fi
    done

    echo ""
    print_success "已停止 $count 个实例"
}

# 删除实例
delete_instance() {
    local name=$1

    if [ -z "$name" ]; then
        print_error "请指定实例名称"
        return 1
    fi

    local instance_dir="$CLUSTER_DIR/$name"

    if [ ! -d "$instance_dir" ]; then
        print_error "实例 '$name' 不存在"
        return 1
    fi

    print_warning "确定要删除实例 '$name' 吗？"
    read -p "确认删除? (yes/no): " confirm

    if [ "$confirm" == "yes" ]; then
        # 停止实例
        cd "$instance_dir"
        ./manage.sh stop > /dev/null 2>&1

        # 删除目录
        cd "$CLUSTER_DIR"
        rm -rf "$name"

        print_success "实例 '$name' 已删除"
    else
        print_info "取消删除"
    fi
}

# 查看集群状态
cluster_status() {
    print_header
    print_info "集群状态："
    echo ""

    if [ ! -d "$CLUSTER_DIR" ]; then
        print_error "集群未初始化"
        return 1
    fi

    local total=0
    local running=0
    local stopped=0

    for instance_dir in "$CLUSTER_DIR"/*/; do
        if [ -d "$instance_dir" ]; then
            local name=$(basename "$instance_dir")
            local config="$instance_dir/config.json"

            if [ -f "$config" ]; then
                total=$((total + 1))
                local port=$(grep -o '"port":[^,]*' "$config" | cut -d: -f2)

                if [ -f "$instance_dir/server.pid" ]; then
                    local pid=$(cat "$instance_dir/server.pid")
                    if ps -p $pid > /dev/null 2>&1; then
                        running=$((running + 1))
                        echo -e "${GREEN}●${NC} $name (端口: $port, PID: $pid)"
                    else
                        stopped=$((stopped + 1))
                        echo -e "${RED}○${NC} $name (端口: $port)"
                    fi
                else
                    stopped=$((stopped + 1))
                    echo -e "${RED}○${NC} $name (端口: $port)"
                fi
            fi
        fi
    done

    echo ""
    echo "总计: $total | 运行中: ${GREEN}$running${NC} | 已停止: ${RED}$stopped${NC}"
}

# 批量部署
batch_deploy() {
    print_header
    print_info "批量部署网站到所有实例..."
    echo ""

    if [ ! -d "$CLUSTER_DIR" ]; then
        print_error "集群未初始化"
        return 1
    fi

    local source_dir="$SCRIPT_DIR"
    local count=0

    for instance_dir in "$CLUSTER_DIR"/*/; do
        if [ -d "$instance_dir" ]; then
            local name=$(basename "$instance_dir")
            print_info "部署到: $name"

            # 复制文件
            cp "$source_dir/index.html" "$instance_dir/" 2>/dev/null
            cp "$source_dir/admin.html" "$instance_dir/" 2>/dev/null
            cp "$source_dir/vercel.json" "$instance_dir/" 2>/dev/null

            # 重启实例
            cd "$instance_dir"
            ./manage.sh restart > /dev/null 2>&1

            count=$((count + 1))
            print_success "✓ $name"
        fi
    done

    echo ""
    print_success "已部署到 $count 个实例"
}

# 显示帮助
show_help() {
    print_header
    echo "使用方法："
    echo ""
    echo "  ./cluster.sh init           - 初始化集群"
    echo "  ./cluster.sh add            - 添加新实例"
    echo "  ./cluster.sh list           - 列出所有实例"
    echo "  ./cluster.sh start <name>   - 启动指定实例"
    echo "  ./cluster.sh stop <name>    - 停止指定实例"
    echo "  ./cluster.sh start-all      - 批量启动所有实例"
    echo "  ./cluster.sh stop-all       - 批量停止所有实例"
    echo "  ./cluster.sh delete <name>  - 删除指定实例"
    echo "  ./cluster.sh status         - 查看集群状态"
    echo "  ./cluster.sh deploy         - 批量部署"
    echo "  ./cluster.sh help           - 显示帮助"
    echo ""
    echo "集群目录: $CLUSTER_DIR"
}

# 主菜单
show_menu() {
    print_header
    echo -e "${MAGENTA}请选择操作：${NC}"
    echo ""
    echo "  1) 初始化集群"
    echo "  2) 添加新实例"
    echo "  3) 列出所有实例"
    echo "  4) 查看集群状态"
    echo "  5) 批量启动所有实例"
    echo "  6) 批量停止所有实例"
    echo "  7) 批量部署"
    echo "  8) 删除实例"
    echo "  9) 退出"
    echo ""
    read -p "请输入选项 (1-9): " choice

    case $choice in
        1)
            init_cluster
            ;;
        2)
            add_instance
            ;;
        3)
            list_instances
            ;;
        4)
            cluster_status
            ;;
        5)
            start_all
            ;;
        6)
            stop_all
            ;;
        7)
            batch_deploy
            ;;
        8)
            list_instances
            echo ""
            read -p "输入要删除的实例名称: " name
            delete_instance "$name"
            ;;
        9)
            print_info "退出..."
            exit 0
            ;;
        *)
            print_error "无效选项"
            ;;
    esac

    echo ""
    read -p "按回车键继续..."
    show_menu
}

# 主流程

if [ $# -eq 0 ]; then
    show_menu
else
    case "$1" in
        init)
            init_cluster
            ;;
        add)
            add_instance
            ;;
        list)
            list_instances
            ;;
        start)
            if [ -z "$2" ]; then
                print_error "请指定实例名称"
                exit 1
            fi
            start_instance "$2"
            ;;
        stop)
            if [ -z "$2" ]; then
                print_error "请指定实例名称"
                exit 1
            fi
            stop_instance "$2"
            ;;
        start-all)
            start_all
            ;;
        stop-all)
            stop_all
            ;;
        delete)
            if [ -z "$2" ]; then
                print_error "请指定实例名称"
                exit 1
            fi
            delete_instance "$2"
            ;;
        status)
            cluster_status
            ;;
        deploy)
            batch_deploy
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            show_help
            ;;
    esac
fi
