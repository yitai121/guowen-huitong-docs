#!/usr/bin/env python3
"""获取国文汇通官网内容"""
import json
import requests
from bs4 import BeautifulSoup

def main():
    """获取网站内容"""
    url = "https://gwht.jscaee.cn"

    try:
        # 获取网页内容
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = response.apparent_encoding

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取标题
            title = soup.title.string if soup.title else "未找到标题"

            # 提取所有文本内容
            text_content = []
            for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span', 'div']):
                text = p.get_text(strip=True)
                if text and len(text) > 10:
                    text_content.append(text)

            # 去重
            text_content = list(dict.fromkeys(text_content))

            # 提取所有图片
            images = []
            for img in soup.find_all('img'):
                src = img.get('src', '')
                alt = img.get('alt', '')
                if src:
                    # 处理相对路径
                    if src.startswith('/'):
                        src = url + src
                    elif not src.startswith('http'):
                        src = url + '/' + src
                    images.append({
                        "url": src,
                        "alt": alt
                    })

            # 提取所有链接
            links = []
            for a in soup.find_all('a'):
                href = a.get('href', '')
                text = a.get_text(strip=True)
                if href:
                    # 处理相对路径
                    if href.startswith('/'):
                        href = url + href
                    elif not href.startswith('http') and not href.startswith('javascript'):
                        href = url + '/' + href
                    links.append({
                        "url": href,
                        "text": text
                    })

            # 保存结果
            result = {
                "title": title.strip(),
                "url": url,
                "status": "success",
                "text_content": text_content[:50],  # 最多保存50条文本
                "images": images[:20],  # 最多保存20张图片
                "links": links[:30],  # 最多保存30个链接
                "total_images": len(images),
                "total_links": len(links),
                "raw_html": response.text[:10000]  # 保存部分原始HTML
            }

            # 保存到文件
            output_path = "/workspace/projects/assets/website_content.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            print(f"✅ 网站内容获取成功！")
            print(f"📄 标题: {title.strip()}")
            print(f"🖼️  图片数量: {len(images)}")
            print(f"🔗 链接数量: {len(links)}")
            print(f"💾 已保存到: {output_path}")

            # 打印部分文本内容供参考
            print("\n" + "="*50)
            print("📝 网站文本内容预览:")
            print("="*50)
            for i, text in enumerate(text_content[:20]):
                print(f"{i+1}. {text[:150]}")

        else:
            print(f"❌ 获取失败，状态码: {response.status_code}")

    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")

if __name__ == "__main__":
    main()
