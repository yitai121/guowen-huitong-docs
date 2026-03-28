#!/bin/bash

# 国文汇通资料管理系统启动脚本

echo "🚀 正在启动国文汇通资料管理系统..."

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    exit 1
fi

# 进入项目目录
cd "$(dirname "$0")/.." || exit 1

echo "📁 当前目录: $(pwd)"

# 检查依赖
echo "📦 检查依赖包..."
if [ -f "requirements.txt" ]; then
    if ! pip3 list | grep -q "supabase"; then
        echo "⚠️  检测到缺少依赖包，正在安装..."
        pip3 install -r requirements.txt
    fi
fi

# 初始化数据库
echo "🗄️  初始化数据库..."
if [ -f "scripts/init_guowen_data.py" ]; then
    python3 scripts/init_guowen_data.py
fi

# 启动自动化任务（后台运行）
echo "⚙️  启动自动化任务..."
nohup python3 scripts/automation.py > /tmp/automation.log 2>&1 &
AUTOMATION_PID=$!
echo "✅ 自动化任务已启动 (PID: $AUTOMATION_PID)"

echo ""
echo "🎉 系统启动完成！"
echo ""
echo "📖 访问方式:"
echo "   打开浏览器访问: assets/index.html"
echo ""
echo "📊 自动化任务状态:"
echo "   查看日志: tail -f /tmp/automation.log"
echo "   停止任务: kill $AUTOMATION_PID"
echo ""
echo "💡 提示:"
echo "   - 首次使用请运行初始化脚本"
echo "   - 确保网络连接正常"
echo "   - 系统会自动定时更新"
echo ""
echo "🚀 开始使用吧！"
