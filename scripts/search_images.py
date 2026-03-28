#!/usr/bin/env python3
"""搜索国文汇通高清图片素材"""
import json
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context

def main():
    """搜索图片素材"""
    ctx = new_context(method="search.image")
    client = SearchClient(ctx=ctx)

    # 搜索不同类型的图片
    search_queries = [
        "国文汇通 Logo 高清",
        "数字藏品平台 展示图",
        "区块链技术 科技感",
        "文化数字化 博物馆",
        "数字资产交易 科技背景",
        "江苏文交所 官网",
        "国文通卷 产品图",
        "文旅消费 场景图",
        "文创产品 展示",
        "中国传统文化 现代化"
    ]

    all_images = {}

    for query in search_queries:
        print(f"\n🔍 正在搜索: {query}")
        print("=" * 60)

        try:
            response = client.image_search(
                query=query,
                count=5
            )

            print(f"✅ 找到 {len(response.image_items)} 张图片")

            images = []
            for item in response.image_items:
                images.append({
                    "title": item.title or "未命名",
                    "source": item.site_name,
                    "url": item.image.url,
                    "width": item.image.width,
                    "height": item.image.height,
                    "shape": item.image.shape
                })

                # 打印图片信息
                print(f"   📸 {item.title or '未命名'}")
                print(f"   📐 {item.image.width}x{item.image.height}")
                print(f"   🔗 {item.image.url[:80]}...")

            all_images[query] = images

        except Exception as e:
            print(f"❌ 搜索失败: {str(e)}")
            all_images[query] = []

    # 保存结果
    output_path = "/workspace/projects/assets/image_search.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_images, f, ensure_ascii=False, indent=2)

    print(f"\n💾 图片搜索结果已保存到: {output_path}")

    # 统计
    total_images = sum(len(imgs) for imgs in all_images.values())
    print(f"\n📊 总共获取 {total_images} 张图片素材")

if __name__ == "__main__":
    main()
