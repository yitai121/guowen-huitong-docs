#!/usr/bin/env python3
"""爬取国文汇通最新资讯"""
import json
from datetime import datetime
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context

def main():
    """爬取最新资讯"""
    ctx = new_context(method="search.news")
    client = SearchClient(ctx=ctx)

    # 搜索最新资讯
    query = "国文汇通 最新动态"
    print(f"🔍 正在搜索: {query}")
    print("=" * 60)

    try:
        response = client.search(
            query=query,
            search_type="web",
            count=10,
            time_range="1m",  # 最近一个月
            need_summary=True
        )

        news_list = []
        for item in response.web_items:
            news_item = {
                "title": item.title,
                "url": item.url,
                "source": item.site_name,
                "date": item.publish_time,
                "summary": item.summary or item.snippet,
                "snippet": item.snippet
            }
            news_list.append(news_item)

            print(f"\n📰 {item.title}")
            print(f"   来源: {item.site_name}")
            print(f"   时间: {item.publish_time}")
            print(f"   摘要: {item.snippet[:100]}...")

        # 保存结果
        result = {
            "total": len(news_list),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "news": news_list
        }

        output_path = "/workspace/projects/assets/news_data.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n💾 资讯已保存到: {output_path}")
        print(f"✅ 共获取 {len(news_list)} 条资讯")

    except Exception as e:
        print(f"❌ 爬取失败: {str(e)}")

if __name__ == "__main__":
    main()
