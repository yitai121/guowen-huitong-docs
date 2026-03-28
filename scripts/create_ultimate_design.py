#!/usr/bin/env python3
"""创建比原站更好的终极设计"""

import time
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage

def create_ultimate_website():
    """创建比原站更好的终极网站设计"""
    ctx = new_context(method="ultimate_design")
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
- transition: 125 次
- backdrop: 0 次（原站没有磨砂效果！）

关键发现：
1. 原站有丰富的动画和过渡效果
2. 原站有大量的渐变背景
3. 原站没有使用磨砂玻璃效果
4. 原站使用 Vue 2.7.14 框架
"""

    system_prompt = f"""你是一位顶级的网站设计大师，精通所有现代设计理念。你的目标是创建一个比 guowenhuitong.com 更好、更现代、更具视觉冲击力的企业官网。

{analysis_report}

设计要求（必须比原站更好）：

1. **Hero 区域渐变背景**（比原站更漂亮）：
   - 使用多层渐变，创造深度感
   - 添加动态渐变动画，让背景"呼吸"
   - 使用更丰富的颜色：紫色、蓝色、粉色混合
   - 添加粒子效果或光晕效果
   - 确保文字可读性

2. **卡片悬停效果**（比原站更流畅）：
   - 3D 倾斜效果（Tilt effect）
   - 多层阴影，营造立体感
   - 平滑的缩放和位移
   - 亮度变化
   - 边框发光效果
   - 使用 cubic-bezier 缓动函数

3. **导航栏磨砂效果**（原站没有！这是你的优势）：
   - 使用 backdrop-filter: blur() 实现磨砂玻璃效果
   - 添加透明度渐变
   - 滚动时动态变化背景透明度
   - 添加细腻的边框和阴影
   - 确保在不同背景上都清晰可见

4. **动画效果**（比原站更高级）：
   - 使用 Intersection Observer 实现滚动触发动画
   - 元素进入视口时的交错淡入效果
   - 数字滚动动画（从 0 滚动到目标值）
   - 视差滚动效果（背景和前景以不同速度移动）
   - 加载动画使用 SVG 路径动画

5. **技术要求**：
   - 纯原生 HTML5, CSS3, JavaScript
   - 无任何框架依赖
   - 所有 CSS 写在 <style> 标签内
   - 所有 JavaScript 写在 <script> 标签内
   - 使用 CSS Variables 管理配色
   - 所有图标使用内联 SVG
   - Logo 使用 assets/logo.png

6. **性能优化**：
   - 使用 GPU 加速动画（transform, opacity）
   - 使用 will-change 优化动画性能
   - 使用 requestAnimationFrame 实现流畅动画
   - 避免重排重绘

配色方案（比原站更现代）：
- 主色：#7C3AED（紫色）
- 辅助色：#3B82F6（蓝色）
- 强调色：#EC4899（粉色）
- 深色：#0F172A
- 浅色：#F8FAFC

设计理念：
- 极简主义但富有视觉冲击力
- 大量留白，但每个元素都有意义
- 流畅的动画，但不过度
- 清晰的视觉层次
- 完美的移动端适配

网站结构：
1. 超级加载动画（Logo 旋转 + 进度条）
2. 磨砂玻璃导航栏（带动态背景）
3. Hero 区域（多层渐变 + 动态光晕 + 粒子效果）
4. 核心业务（3D 卡片 + 悬停发光）
5. 运营中心（数字滚动 + 动态图表）
6. 新闻资讯（卡片悬停 + 图片放大）
7. 视频模块（沉浸式播放器）
8. 页脚（渐变背景 + 磨砂效果）

直接输出完整 HTML 代码，不要代码块标记。"""

    user_prompt = """为国文汇通创建比原站更好的终极官网。

信息：
- 名称：国文汇通
- Logo：assets/logo.png（245KB PNG）
- 宣传语：以文化为魂·以科技为器·以金融为力，让中华文化数字化、资产化、全球化
- 下载：https://x.gwht.jscaee.cn
- 官网：https://www.guowenhuitong.com

核心业务：
1. 数字藏品交易 - 安全合规的数字藏品交易平台，支持各类文化数字资产的发行、交易、收藏
2. 文化产权交易 - 规范的文化产权交易体系，为文化IP、著作权提供评估、交易、融资服务
3. 数字资产服务 - 专业的数字资产存证、确权、评估服务，运用区块链技术保障资产安全

运营数据：
- 注册用户：100万+
- 合作IP方：500+
- 上线藏品：3000+
- 系统可用率：99.9%

新闻内容：
1. 国文汇通与多家文化机构达成战略合作，共同推动数字文化产业发展
2. 平台全新版本上线，优化交易体验，大幅提升用户满意度
3. 数字文化产业发展论坛成功举办，行业专家齐聚探讨发展机遇

关键要求（必须比原站更好）：
1. Hero 区域使用多层动态渐变背景，比原站更漂亮
2. 卡片悬停效果更流畅，添加 3D 效果和发光边框
3. 导航栏使用磨砂玻璃效果（原站没有）
4. 动画更流畅，性能更好
5. 整体视觉效果更现代、更震撼

直接输出 HTML 代码。"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    print("=" * 60)
    print("正在创建比原站更好的终极设计...")
    print("=" * 60)

    # 使用 streaming 来避免超时
    full_content = ""
    for chunk in client.stream(
        messages=messages,
        model="doubao-seed-2-0-pro-260215",
        temperature=0.8,
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
    print("✅ 终极设计创建完成！")
    print("="*60)
    print(f"文件大小: {len(html_content)} 字符")
    print(f"文件行数: {len(html_content.split(chr(10)))} 行")
    print("="*60)

if __name__ == "__main__":
    create_ultimate_website()
