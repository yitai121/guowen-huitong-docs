#!/usr/bin/env python3
"""分析参考网站 guowenhuitong.com"""
import json
import requests
from bs4 import BeautifulSoup

def main():
    """获取参考网站内容"""
    url = "https://guowenhuitong.com"

    try:
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

            text_content = list(dict.fromkeys(text_content))

            # 提取所有图片
            images = []
            for img in soup.find_all('img'):
                src = img.get('src', '') or img.get('data-src', '')
                alt = img.get('alt', '')
                if src:
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
                "text_content": text_content[:50],
                "images": images[:30],
                "links": links[:50],
                "total_images": len(images),
                "total_links": len(links),
                "nav_menu": [],
                "sections": []
            }

            # 尝试提取导航菜单
            nav_items = soup.find_all('nav')
            for nav in nav_items:
                for a in nav.find_all('a'):
                    text = a.get_text(strip=True)
                    href = a.get('href', '')
                    if text and href:
                        result["nav_menu"].append({
                            "text": text,
                            "href": href if href.startswith('http') else url + href
                        })

            # 保存到文件
            output_path = "/workspace/projects/assets/reference_site.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            print(f"✅ 参考网站分析成功！")
            print(f"📄 标题: {title.strip()}")
            print(f"🖼️  图片数量: {len(images)}")
            print(f"🔗 链接数量: {len(links)}")
            print(f"📋 导航项: {len(result['nav_menu'])}")
            print(f"💾 已保存到: {output_path}")

            # 打印导航菜单
            print("\n" + "="*50)
            print("📋 导航菜单:")
            print("="*50)
            for i, item in enumerate(result['nav_menu'][:10], 1):
                print(f"{i}. {item['text']} - {item['href']}")

        else:
            print(f"❌ 获取失败，状态码: {response.status_code}")

    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")

if __name__ == "__main__":
    main()
