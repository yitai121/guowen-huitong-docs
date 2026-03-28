#!/usr/bin/env python3
"""深度分析 guowenhuitong.com"""
import json
import requests
from bs4 import BeautifulSoup

def main():
    """深度分析参考网站"""
    url = "https://www.guowenhuitong.com"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = response.apparent_encoding

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # 分析标题
            title = soup.title.string if soup.title else "未找到标题"

            # 提取所有样式类名
            all_classes = set()
            for tag in soup.find_all(True):
                if tag.get('class'):
                    all_classes.update(tag.get('class'))

            # 提取导航菜单
            nav_menus = []
            nav = soup.find('nav') or soup.find(class_=lambda x: x and ('nav' in str(x).lower() or 'menu' in str(x).lower()))
            if nav:
                for a in nav.find_all('a'):
                    text = a.get_text(strip=True)
                    href = a.get('href', '')
                    if text and href:
                        nav_menus.append({'text': text, 'href': href if href.startswith('http') else url + href})

            # 提取 Hero 区域
            hero_section = []
            hero = soup.find(class_=lambda x: x and 'hero' in str(x).lower()) or soup.find('section', class_=lambda x: x and 'banner' in str(x).lower()) or soup.find('div', class_=lambda x: x and ('top' in str(x).lower() or 'header' in str(x).lower()))
            if hero:
                hero_section.append({
                    'tag': str(hero.name),
                    'class': hero.get('class', []),
                    'text': hero.get_text(strip=True)[:500]
                })

            # 提取所有图片（排除loading图片）
            images = []
            for img in soup.find_all('img'):
                src = img.get('src', '') or img.get('data-src', '') or img.get('data-original', '')
                alt = img.get('alt', '')
                width = img.get('width', '')
                height = img.get('height', '')
                if src and not 'loading' in src and not 'dot.gif' in src:
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        src = url + src
                    elif not src.startswith('http'):
                        src = url + '/' + src
                    images.append({
                        "url": src,
                        "alt": alt,
                        "width": width,
                        "height": height
                    })

            # 提取所有视频
            videos = []
            for video in soup.find_all('video'):
                src = video.get('src', '')
                poster = video.get('poster', '')
                if src:
                    if src.startswith('/'):
                        src = url + src
                    elif not src.startswith('http'):
                        src = url + '/' + src
                    videos.append({
                        "src": src,
                        "poster": poster
                    })

            # 提取 iframe 视频嵌入
            for iframe in soup.find_all('iframe'):
                src = iframe.get('src', '')
                if 'youtube' in src or 'vimeo' in src or 'bilibili' in src:
                    videos.append({
                        "type": "embed",
                        "src": src
                    })

            # 提取核心板块
            sections = []
            for section in soup.find_all(['section', 'div'], class_=True):
                classes = section.get('class', [])
                class_str = ' '.join(classes) if classes else ''
                if any(keyword in class_str.lower() for keyword in ['core', 'business', 'service', 'advantage', 'vision', 'practice', 'operation']):
                    section_title = section.find(['h1', 'h2', 'h3'])
                    title_text = section_title.get_text(strip=True) if section_title else ''
                    sections.append({
                        'class': classes,
                        'title': title_text,
                        'content': section.get_text(strip=True)[:300]
                    })

            # 保存结果
            result = {
                "url": url,
                "title": title.strip(),
                "nav_menus": nav_menus,
                "hero_section": hero_section,
                "images": images[:20],
                "total_images": len(images),
                "videos": videos,
                "total_videos": len(videos),
                "sections": sections[:10],
                "unique_classes": sorted(list(all_classes))[:50],
                "color_schemes": []
            }

            output_path = "/workspace/projects/assets/deep_analysis.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            print(f"✅ 深度分析完成！")
            print(f"📄 标题: {title.strip()}")
            print(f"📋 导航项: {len(nav_menus)}")
            print(f"🖼️  图片: {len(images)}")
            print(f"🎬 视频: {len(videos)}")
            print(f"📦 板块: {len(sections)}")
            print(f"💾 已保存到: {output_path}")

            # 打印导航菜单
            print("\n" + "="*60)
            print("📋 导航菜单:")
            print("="*60)
            for i, item in enumerate(nav_menus, 1):
                print(f"{i}. {item['text']} - {item['href']}")

            # 打印图片
            print("\n" + "="*60)
            print("🖼️  主要图片:")
            print("="*60)
            for i, img in enumerate(images[:10], 1):
                print(f"{i}. {img['alt'][:50]} - {img['url'][:80]}...")

            # 打印视频
            if videos:
                print("\n" + "="*60)
                print("🎬 视频:")
                print("="*60)
                for i, vid in enumerate(videos, 1):
                    print(f"{i}. {vid.get('type', 'video')} - {vid.get('src', '')[:80]}...")

        else:
            print(f"❌ 获取失败，状态码: {response.status_code}")

    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
