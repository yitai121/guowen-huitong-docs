#!/usr/bin/env python3
"""分析头部企业官网设计"""

from coze_coding_dev_sdk import SearchClient, LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import SystemMessage, HumanMessage

def analyze_top_company_designs():
    """分析头部企业官网设计特点"""
    ctx = new_context(method="analyze_designs")
    search_client = SearchClient(ctx=ctx)
    llm_client = LLMClient(ctx=ctx)

    print("=" * 60)
    print("搜索头部企业官网设计...")
    print("=" * 60)

    # 搜索 Apple 设计
    print("\n1. 搜索 Apple 官网设计...")
    apple_response = search_client.web_search(
        query="Apple 官网设计特点 动画 UI 设计",
        count=5,
        need_summary=True
    )

    # 搜索 Google 设计
    print("2. 搜索 Google 官网设计...")
    google_response = search_client.web_search(
        query="Google 官网设计 Material Design 交互",
        count=5,
        need_summary=True
    )

    # 搜索 Microsoft 设计
    print("3. 搜索 Microsoft 官网设计...")
    microsoft_response = search_client.web_search(
        query="Microsoft Fluent Design 官网设计风格",
        count=5,
        need_summary=True
    )

    # 搜索企业官网设计最佳实践
    print("4. 搜索企业官网设计最佳实践...")
    best_practices_response = search_client.web_search(
        query="企业官网设计最佳实践 2024 动画效果",
        count=5,
        need_summary=True
    )

    print("\n" + "=" * 60)
    print("正在使用 LLM 综合分析...")
    print("=" * 60)

    # 使用 LLM 综合分析
    analysis_prompt = f"""你是一位顶级网站设计专家。请基于以下搜索结果，分析头部企业官网的设计特点：

Apple 官网设计：
{apple_response.summary if apple_response.summary else ''}

Google 官网设计：
{google_response.summary if google_response.summary else ''}

Microsoft 官网设计：
{microsoft_response.summary if microsoft_response.summary else ''}

企业官网设计最佳实践：
{best_practices_response.summary if best_practices_response else ''}

请总结以下要点：
1. 头部企业官网的设计核心理念
2. 常用的动画效果和交互方式
3. 配色方案和视觉层次
4. 布局结构和导航设计
5. 移动端适配策略

请以专业、简洁的方式输出分析结果。"""

    messages = [
        SystemMessage(content="你是一位顶级的网站设计专家，精通 Apple、Google、Microsoft 等头部企业的设计理念。"),
        HumanMessage(content=analysis_prompt)
    ]

    response = llm_client.invoke(
        messages=messages,
        model="doubao-seed-2-0-pro-260215",
        temperature=0.5
    )

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

    print("\n" + "=" * 60)
    print("头部企业官网设计分析")
    print("=" * 60)
    print(get_text_content(response.content))
    print("=" * 60)

    # 保存分析结果
    with open("assets/design_analysis.txt", "w", encoding="utf-8") as f:
        f.write(get_text_content(response.content))

    print("\n分析结果已保存到: assets/design_analysis.txt")

if __name__ == "__main__":
    analyze_top_company_designs()
