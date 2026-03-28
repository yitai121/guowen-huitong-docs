#!/usr/bin/env python3
"""创建高质量的网站设计 - 基于头部企业设计理念"""

import time
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage

def create_premium_website():
    """创建高质量的网站设计"""
    ctx = new_context(method="premium_design")
    client = LLMClient(ctx=ctx)

    system_prompt = """你是一位顶级网站设计师，精通 Apple、Google、Microsoft 的设计理念。

设计核心理念：
- 极简主义，大量留白
- 流畅的滚动动画
- SVG 图标（不使用表情符号）
- 高级 CSS 动画
- Logo 使用 assets/logo.png

技术要求：
- 纯原生 HTML/CSS/JS
- 所有 SVG 图标内联
- 使用 Intersection Observer 实现滚动动画
- 平滑滚动、悬停效果、加载动画

网站结构：
1. 加载动画
2. 导航栏（磨砂玻璃效果）
3. Hero 区域（大标题 + CTA）
4. 核心业务（卡片 + 悬停）
5. 运营中心（数字滚动）
6. 新闻资讯（列表）
7. 视频模块
8. 页脚

直接输出完整 HTML 代码，不要代码块标记。"""

    user_prompt = """为国文汇通创建高质量官网。

信息：
- 名称：国文汇通
- Logo：assets/logo.png
- 宣传语：以文化为魂·以科技为器·以金融为力，让中华文化数字化、资产化、全球化
- 下载：https://x.gwht.jscaee.cn

业务：
1. 数字藏品交易
2. 文化产权交易
3. 数字资产服务

数据：
- 注册用户：100万+
- 合作IP方：500+
- 上线藏品：3000+
- 系统可用率：99.9%

要求：
- 流畅动画
- SVG 图标
- Logo 正确显示
- 响应式设计

直接输出 HTML 代码。"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    print("正在创建高质量网站...")

    # 使用 streaming 来避免超时
    full_content = ""
    for chunk in client.stream(
        messages=messages,
        model="doubao-seed-2-0-pro-260215",
        temperature=0.7,
        max_completion_tokens=16384
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

    print(f"\n\n✅ 网站创建完成！文件大小: {len(html_content)} 字符")

if __name__ == "__main__":
    create_premium_website()
