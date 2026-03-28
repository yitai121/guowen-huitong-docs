#!/usr/bin/env python3
"""搜索国文汇通相关资料"""
import json
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context

def main():
    """搜索公司信息"""
    ctx = new_context(method="search.web")
    client = SearchClient(ctx=ctx)

    # 搜索国文汇通相关信息
    queries = [
        "国文汇通 数字藏品",
        "江苏文化产权交易所 国文汇通",
        "国文汇通 NFT 平台",
        "国文汇通 公司介绍",
        "gwht.jscaee.cn 国文汇通"
    ]

    all_results = {}

    for query in queries:
        print(f"\n🔍 正在搜索: {query}")
        print("=" * 60)

        try:
            response = client.web_search_with_summary(
                query=query,
                count=10
            )

            print(f"✅ 找到 {len(response.web_items)} 条结果")

            # 提取结果
            results = []
            for item in response.web_items:
                results.append({
                    "title": item.title,
                    "url": item.url,
                    "snippet": item.snippet,
                    "site_name": item.site_name,
                    "publish_time": item.publish_time,
                    "summary": item.summary
                })

            all_results[query] = {
                "count": len(results),
                "summary": response.summary,
                "results": results
            }

            # 打印部分结果
            for i, item in enumerate(results[:5], 1):
                print(f"\n{i}. {item['title']}")
                print(f"   来源: {item['site_name']}")
                print(f"   摘要: {item['snippet'][:150]}...")

        except Exception as e:
            print(f"❌ 搜索失败: {str(e)}")
            all_results[query] = {"error": str(e)}

    # 保存结果
    output_path = "/workspace/projects/assets/company_search.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n💾 搜索结果已保存到: {output_path}")

if __name__ == "__main__":
    main()
