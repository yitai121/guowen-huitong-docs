#!/usr/bin/env python3
"""创建比原站更好的终极设计 - 纯原生版本"""

import time
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage

def create_ultimate_native_website():
    """创建比原站更好的纯原生终极网站设计"""
    ctx = new_context(method="ultimate_native")
    client = LLMClient(ctx=ctx)

    # 基于我的分析结果
    analysis_report = """
基于对 guowenhuitong.com 的深度分析：

CSS 分析结果：
- 总大小：1,104,123 字符
- 渐变背景：77 处
- 动画定义：433 处
- 过渡效果：455 处
- 磨砂效果：0 处（原站没有使用磨砂效果！）

JavaScript 分析结果：
- 总大小：2,673,090 字符
- animate: 350 次
- animation: 513 次
- hover: 692 次
- scroll: 853 次
- backdrop: 0 次（原站没有磨砂效果！）

关键发现：
1. 原站有丰富的动画和过渡效果
2. 原站有大量的渐变背景
3. 原站没有使用磨砂玻璃效果
4. 原站使用 Vue 2.7.14 框架
"""

    system_prompt = f"""你是一位顶级的网站设计大师。你的目标是创建一个比 guowenhuitong.com 更好的企业官网。

{analysis_report}

**严格要求**（违反即不合格）：
1. 必须使用纯原生 HTML5, CSS3, JavaScript
2. 严禁使用任何框架（Tailwind CSS, Bootstrap, Vue, React, Angular 等）
3. 严禁使用任何外部 CSS 库
4. 严禁使用任何外部图标库（Font Awesome 等）
5. 严禁使用任何 CDN 链接
6. 所有 CSS 必须写在 <style> 标签内
7. 所有 JavaScript 必须写在 <script> 标签内
8. 所有图标必须使用内联 SVG（不使用外部文件）
9. Logo 使用 assets/logo.png

设计要求（必须比原站更好）：

1. **Hero 区域渐变背景**（比原站更漂亮）：
   - 使用 3 层径向渐变叠加
   - 添加背景位置动画，让渐变"呼吸"
   - 颜色：#7C3AED（紫色）+ #3B82F6（蓝色）+ #EC4899（粉色）
   - 添加浮动的粒子效果（使用 CSS 动画）

2. **卡片悬停效果**（比原站更流畅）：
   - 3D 倾斜效果（JavaScript 计算鼠标位置）
   - 多层阴影，营造立体感
   - 边框发光效果（使用伪元素）
   - 平滑的缩放和位移
   - 使用 cubic-bezier(0.23, 1, 0.320, 1) 缓动函数

3. **导航栏磨砂效果**（原站没有！）：
   - 使用 backdrop-filter: blur(20px) 实现磨砂玻璃
   - 添加 rgba 背景色
   - 滚动时动态调整背景透明度（JavaScript）
   - 添加细腻的边框
   - 确保文字清晰可读

4. **动画效果**（比原站更高级）：
   - 使用 IntersectionObserver 实现滚动触发动画
   - 元素进入视口时淡入上移
   - 数字滚动动画（requestAnimationFrame）
   - 视差滚动效果（监听 scroll 事件）
   - 加载动画：Logo 旋转 + 进度条

5. **性能优化**：
   - 使用 transform 和 opacity（GPU 加速）
   - 使用 will-change 优化
   - 使用 requestAnimationFrame
   - 避免修改 layout 属性

6. **配色方案**：
   - 主色：#7C3AED（紫色）
   - 辅助色：#3B82F6（蓝色）
   - 强调色：#EC4899（粉色）
   - 深色：#0F172A
   - 浅色：#F8FAFC

网站结构：
1. 加载动画（Logo + 进度条）
2. 磨砂玻璃导航栏
3. Hero 区域（多层渐变 + 粒子）
4. 核心业务（3D 卡片）
5. 运营中心（数字滚动）
6. 新闻资讯（悬停效果）
7. 视频模块
8. 页脚

直接输出完整 HTML 代码，不要代码块标记。"""

    user_prompt = """为国文汇通创建比原站更好的纯原生终极官网。

信息：
- 名称：国文汇通
- Logo：assets/logo.png（245KB PNG）
- 宣传语：以文化为魂·以科技为器·以金融为力，让中华文化数字化、资产化、全球化
- 下载：https://x.gwht.jscaee.cn
- 官网：https://www.guowenhuitong.com

核心业务：
1. 数字藏品交易 - 安全合规的数字藏品交易平台
2. 文化产权交易 - 规范的文化产权交易服务
3. 数字资产服务 - 专业的数字资产存证、确权、评估服务

运营数据：
- 注册用户：100万+
- 合作IP方：500+
- 上线藏品：3000+
- 系统可用率：99.9%

新闻：
1. 国文汇通与多家文化机构达成战略合作
2. 平台全新版本上线，优化交易体验
3. 数字文化产业发展论坛成功举办

严格要求：
- 纯原生 HTML/CSS/JS
- 无任何框架
- 无外部依赖
- 磨砂玻璃导航栏
- 多层渐变背景
- 3D 卡片悬停
- 流畅动画

直接输出 HTML 代码。"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    print("=" * 60)
    print("正在创建比原站更好的纯原生终极设计...")
    print("=" * 60)

    # 使用 streaming
    full_content = ""
    for chunk in client.stream(
        messages=messages,
        model="doubao-seed-2-0-pro-260215",
        temperature=0.7,
        max_completion_tokens=32768
    ):
        if chunk.content:
            if isinstance(chunk.content, str):
                print(chunk.content, end="", flush=True)
                full_content += chunk.content
            elif isinstance(chunk.content, list):
                for item in chunk.content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text = item.get("text", "")
                        print(text, end="", flush=True)
                        full_content += text

    # 去除代码块标记
    html_content = full_content
    if html_content.startswith("```"):
        first_newline = html_content.find("\n")
        if first_newline != -1:
            html_content = html_content[first_newline+1:]
        last_backticks = html_content.rfind("```")
        if last_backticks != -1:
            html_content = html_content[:last_backticks]

    # 保存到文件
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content.strip())

    print(f"\n\n{'='*60}")
    print("✅ 纯原生终极设计创建完成！")
    print("="*60)
    print(f"文件大小: {len(html_content)} 字符")
    print(f"文件行数: {len(html_content.split(chr(10)))} 行")
    print("="*60)

if __name__ == "__main__":
    create_ultimate_native_website()
