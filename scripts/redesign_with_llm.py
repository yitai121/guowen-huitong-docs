#!/usr/bin/env python3
"""使用顶尖 LLM 重新设计国文汇通网站"""

from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage

def main():
    ctx = new_context(method="redesign")
    client = LLMClient(ctx=ctx)

    system_prompt = """你是一位顶尖的网站设计师和前端开发专家。你需要为一个数字资产文化版权平台设计一个现代、专业、简洁的企业官网。

设计要求：
1. 不要使用任何表情符号
2. 取消实时行情价格展示功能
3. Logo使用本地文件: assets/logo.png
4. 采用极简主义设计，白色背景为主
5. 使用专业的配色方案：紫色（#6366f1）和蓝色（#3b82f6）渐变
6. 所有模块都要有清晰的视觉层次
7. 响应式设计，适配各种设备
8. 代码规范，语义化标签
9. 包含以下模块：
   - 导航栏（Logo + 导航链接）
   - Hero区域（主标题 + 副标题 + CTA按钮）
   - 核心服务（3-4个服务卡片）
   - 运营中心（运营数据展示）
   - 新闻资讯（列表展示）
   - 视频模块（视频播放区域）
   - 页脚（联系信息 + 链接）

技术要求：
- 使用原生 HTML5, CSS3, JavaScript
- 不使用任何框架
- 代码放在一个 HTML 文件中（包含 CSS 和 JS）
- 添加平滑滚动效果
- 添加 hover 动画效果
- 添加页面加载动画"""

    user_prompt = """请为"国文汇通"数字资产文化版权平台生成一个完整的、专业的、现代的 HTML 网站。

网站信息：
- 名称：国文汇通
- 官网：https://www.guowenhuitong.com
- 下载地址：https://x.gwht.jscaee.cn
- 宣传语：以文化为魂·以科技为器·以金融为力，让中华文化数字化、资产化、全球化
- 定位：数字资产文化版权购物商城

核心业务：
- 数字藏品交易
- 文化产权交易
- 数字资产服务

请生成完整的 HTML 代码，包含所有 CSS 样式和 JavaScript 代码。不要使用表情符号，不要包含实时行情功能。"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    print("正在使用顶尖模型重新设计网站...")
    print("使用模型: doubao-seed-2-0-pro-260215\n")

    response = client.invoke(
        messages=messages,
        model="doubao-seed-2-0-pro-260215",
        temperature=0.7,
        max_completion_tokens=32768
    )

    # 提取文本内容
    def get_text_content(content):
        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            if content and isinstance(content[0], str):
                return " ".join(content)
            else:
                text_parts = [item.get("text", "") for item in content if isinstance(item, dict) and item.get("type") == "text"]
                return " ".join(text_parts)
        return str(content)

    html_content = get_text_content(response.content)

    # 保存到文件
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("\n网站重新设计完成！")
    print("文件已保存到: index.html")

if __name__ == "__main__":
    main()
