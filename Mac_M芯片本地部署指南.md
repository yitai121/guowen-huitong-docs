# 🍎 Mac M 芯片 - 本地部署完整指南

## 📋 前置要求

### 系统要求：
- ✅ macOS（M 芯片：M1、M2、M3）
- ✅ 终端（Terminal）
- ✅ Python 3（通常已预装）

### 检查 Python：
```bash
# 打开终端，检查 Python 版本
python3 --version

# 如果显示版本号（如 Python 3.12.x），说明已安装
```

---

## 🚀 部署步骤

### 第一步：准备项目文件

#### 1. 创建项目目录
```bash
# 打开终端
cd ~
mkdir guowen-huitong-website
cd guowen-huitong-website
```

#### 2. 创建必要的文件

**方式 A：从 GitHub 下载（推荐）**
```bash
# 如果有 GitHub 仓库
git clone https://github.com/yitai121/guowen-huitong-docs.git
cd guowen-huitong-docs
```

**方式 B：手动创建文件**

创建以下文件：

**index.html**（主页）
```bash
# 从现有项目复制 index.html 文件到当前目录
```

**admin.html**（管理后台）
```bash
# 从现有项目复制 admin.html 文件到当前目录
```

**vercel.json**（配置文件）
```bash
# 从现有项目复制 vercel.json 文件到当前目录
```

---

### 第二步：创建管理脚本

#### 创建 `manage.sh` 文件：
```bash
cat > manage.sh << 'EOF'
#!/bin/bash

# 配置
PROJECT_DIR=$(pwd)
PORT=8000
LOG_FILE="app.log"
PID_FILE="server.pid"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 函数

print_header() {
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}           ${GREEN}🚀 国文汇通 - 本地管理系统${NC}              ${CYAN}║${NC}"
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

check_server() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p $pid > /dev/null 2>&1; then
            echo "running"
        else
            echo "stopped"
        fi
    else
        echo "stopped"
    fi
}

start_server() {
    print_header
    print_info "正在启动服务器..."

    local status=$(check_server)
    if [ "$status" == "running" ]; then
        print_info "服务器已经在运行中"
        print_info "访问地址: ${GREEN}http://localhost:$PORT${NC}"
    else
        # 启动服务器
        nohup python3 -m http.server $PORT > $LOG_FILE 2>&1 &
        local pid=$!
        echo $pid > $PID_FILE

        sleep 2

        if [ "$(check_server)" == "running" ]; then
            print_success "服务器启动成功！"
            print_info "访问地址: ${GREEN}http://localhost:$PORT${NC}"
            print_info "日志文件: ${GREEN}$LOG_FILE${NC}"
            print_info "进程 PID: ${GREEN}$pid${NC}"
        else
            print_error "服务器启动失败"
            print_info "查看日志: tail -n 20 $LOG_FILE"
            return 1
        fi
    fi
}

stop_server() {
    print_header
    print_info "正在停止服务器..."

    local status=$(check_server)
    if [ "$status" == "stopped" ]; then
        print_info "服务器已经停止"
    else
        local pid=$(cat "$PID_FILE")
        kill $pid
        rm -f "$PID_FILE"

        sleep 1

        if [ "$(check_server)" == "stopped" ]; then
            print_success "服务器已停止"
        else
            print_error "服务器停止失败"
            return 1
        fi
    fi
}

restart_server() {
    print_header
    print_info "正在重启服务器..."
    stop_server
    sleep 1
    start_server
}

status() {
    print_header

    print_info "系统状态："
    echo ""

    # 服务器状态
    local status=$(check_server)
    echo -e "服务器状态: ${GREEN}${status}${NC}"

    if [ "$status" == "running" ]; then
        echo -e "访问地址: ${GREEN}http://localhost:$PORT${NC}"
        echo -e "日志文件: ${GREEN}$LOG_FILE${NC}"

        if [ -f "$PID_FILE" ]; then
            echo -e "进程 PID: ${GREEN}$(cat $PID_FILE)${NC}"
        fi
    fi

    echo ""

    # 文件检查
    print_info "文件检查："

    if [ -f "index.html" ]; then
        echo -e "  ${GREEN}✓${NC} index.html"
    else
        echo -e "  ${RED}✗${NC} index.html"
    fi

    if [ -f "admin.html" ]; then
        echo -e "  ${GREEN}✓${NC} admin.html"
    else
        echo -e "  ${RED}✗${NC} admin.html"
    fi

    if [ -f "vercel.json" ]; then
        echo -e "  ${GREEN}✓${NC} vercel.json"
    else
        echo -e "  ${RED}✗${NC} vercel.json"
    fi
}

show_logs() {
    print_header
    print_info "最近日志："
    echo ""
    tail -n 20 $LOG_FILE 2>/dev/null || echo "日志文件不存在"
}

show_help() {
    print_header
    echo "使用方法："
    echo ""
    echo "  ./manage.sh start   - 启动服务器"
    echo "  ./manage.sh stop    - 停止服务器"
    echo "  ./manage.sh restart - 重启服务器"
    echo "  ./manage.sh status  - 查看状态"
    echo "  ./manage.sh logs    - 查看日志"
    echo "  ./manage.sh help    - 显示帮助"
    echo ""
    echo "访问地址："
    echo "  http://localhost:$PORT"
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
    logs)
        show_logs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_header
        show_help
        ;;
esac
EOF
```

#### 添加执行权限：
```bash
chmod +x manage.sh
```

---

### 第三步：启动服务器

```bash
./manage.sh start
```

---

### 第四步：访问网站

**在浏览器打开：**
```
http://localhost:8000
```

**你会看到：**
- 🌈 浮动的彩色球体背景
- ✨ 漂浮的白色粒子效果
- 💎 毛玻璃卡片设计
- 🚀 紫蓝粉渐变按钮

---

### 第五步：访问管理后台

**在浏览器打开：**
```
http://localhost:8000/admin.html
```

**登录信息：**
- 用户名：`admin`
- 密码：`admin888`

---

## 🎮 常用命令

```bash
# 查看状态
./manage.sh status

# 启动服务器
./manage.sh start

# 停止服务器
./manage.sh stop

# 重启服务器
./manage.sh restart

# 查看日志
./manage.sh logs

# 显示帮助
./manage.sh help
```

---

## 🔧 故障排除

### 问题 1：端口被占用

**错误信息：**
```
Address already in use
```

**解决方法：**
```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>

# 重新启动
./manage.sh start
```

---

### 问题 2：Python 未安装

**解决方法：**
```bash
# 安装 Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Python
brew install python3
```

---

### 问题 3：权限问题

**解决方法：**
```bash
# 添加执行权限
chmod +x manage.sh

# 如果仍然失败
sudo chmod +x manage.sh
```

---

## 📊 项目结构

```
guowen-huitong-website/
├── index.html              # 主页
├── admin.html              # 管理后台
├── vercel.json             # 配置文件
├── manage.sh               # 管理脚本
├── app.log                 # 日志文件
├── server.pid              # 进程 ID
└── README.md               # 说明文档
```

---

## 🌍 外网访问（可选）

### 使用 ngrok

```bash
# 安装 ngrok
brew install ngrok/ngrok/ngrok

# 启动 ngrok
ngrok http 8000
```

这会生成一个临时的公网 URL。

---

## ✅ 验证部署

运行以下命令检查所有文件：
```bash
./manage.sh status
```

应该看到：
- ✓ index.html
- ✓ admin.html
- ✓ vercel.json

---

## 🎉 完成！

**你的网站已经在本地成功运行了！**

**访问地址：**
```
http://localhost:8000
```

**管理后台：**
```
http://localhost:8000/admin.html
```

---

## 📞 需要帮助？

如果遇到问题：
1. 运行 `./manage.sh status` 查看状态
2. 运行 `./manage.sh logs` 查看日志
3. 检查防火墙设置

---

**现在就启动你的网站吧！**
```bash
./manage.sh start
```

**享受你的动态网站！** 🚀
