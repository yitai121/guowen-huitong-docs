#!/usr/bin/env python3
"""使用顶尖 LLM 重新设计国文汇通网站 - 纯原生版本"""

from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage

def main():
    ctx = new_context(method="redesign")
    client = LLMClient(ctx=ctx)

    system_prompt = """你是一位顶尖的网站设计师和前端开发专家。你需要为一个数字资产文化版权平台设计一个现代、专业、简洁的企业官网。

严格的设计要求：
1. 必须使用纯原生 HTML5, CSS3, JavaScript（严禁使用任何框架如 Tailwind CSS, Bootstrap, Vue, React 等）
2. 所有 CSS 样式必须写在 <style> 标签内
3. 所有 JavaScript 代码必须写在 <script> 标签内
4. 不要使用任何表情符号、Emoji 字符或 Unicode 符号
5. 严禁包含实时行情、价格展示、涨跌幅等任何价格相关功能
6. Logo 必须使用本地文件: assets/logo.png
7. 不使用任何外部图标库（如 Font Awesome），如果需要图标使用纯 CSS 绘制或 SVG
8. 采用极简主义设计，白色背景为主
9. 使用专业的配色方案：紫色（#6366f1）和蓝色（#3b82f6）渐变
10. 所有模块都要有清晰的视觉层次
11. 响应式设计，适配各种设备
12. 代码规范，语义化标签

网站结构要求：
- 导航栏（Logo + 导航链接 + 下载按钮）
- Hero区域（主标题 + 副标题 + CTA按钮）
- 核心服务（3-4个服务卡片）
- 运营中心（运营数据展示）
- 新闻资讯（列表展示）
- 视频模块（视频播放区域）
- 页脚（联系信息 + 链接）

技术要求：
- 添加平滑滚动效果
- 添加 hover 动画效果
- 添加页面加载动画
- 导航栏滚动时添加背景和阴影
- 移动端适配（汉堡菜单）

输出要求：
- 直接输出完整的 HTML 代码，不要有任何解释文字
- 不要使用代码块标记（不要用 ```html ... ```）
- 代码必须是完整的、可运行的
- 不要包含任何表情符号"""

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

运营数据（运营中心展示）：
- 注册用户：100万+
- 合作IP方：500+
- 上线藏品：3000+
- 系统可用率：99.9%

新闻内容：
1. 国文汇通与多家文化机构达成战略合作
2. 平台全新版本上线，优化交易体验
3. 数字文化产业发展论坛成功举办

视频内容：
- 平台介绍视频

请直接生成完整的 HTML 代码。"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    print("正在使用顶尖模型重新设计网站...")
    print("使用模型: doubao-seed-2-0-pro-260215\n")

    response = client.invoke(
        messages=messages,
        model="doubao-seed-2-0-pro-260215",
        temperature=0.5,
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

    # 如果内容以 ``` 开头，去除代码块标记
    if html_content.startswith("```"):
        # 找到第一个换行符
        first_newline = html_content.find("\n")
        if first_newline != -1:
            html_content = html_content[first_newline+1:]
        # 找到最后一个 ```
        last_backticks = html_content.rfind("```")
        if last_backticks != -1:
            html_content = html_content[:last_backticks]

    # 保存到文件
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content.strip())

    print("\n网站重新设计完成！")
    print("文件已保存到: index.html")
    print(f"文件大小: {len(html_content)} 字符")

if __name__ == "__main__":
    main()
