#!/usr/bin/env python3
"""提取所有 CSS 文件"""

import requests
from bs4 import BeautifulSoup
import re
import os

def extract_css_files():
    """提取所有 CSS 文件"""
    url = "https://www.guowenhuitong.com"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print("=" * 60)
    print("提取所有 CSS 文件")
    print("=" * 60)

    # 获取网页内容
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 创建保存 CSS 的目录
    os.makedirs('assets/css', exist_ok=True)

    # 查找所有 <link rel="stylesheet"> 标签
    css_links = soup.find_all('link', rel='stylesheet')

    print(f"\n发现 {len(css_links)} 个 CSS 文件链接\n")

    extracted_css = []

    for i, link in enumerate(css_links, 1):
        href = link.get('href', '')
        print(f"{i}. {href}")

        # 构建完整的 URL
        if href.startswith('//'):
            css_url = 'https:' + href
        elif href.startswith('/'):
            css_url = url + href
        elif href.startswith('http'):
            css_url = href
        else:
            print(f"   ⚠️  无法识别的 URL 格式，跳过")
            continue

        # 下载 CSS 文件
        try:
            css_response = requests.get(css_url, headers=headers, timeout=10)
            css_response.raise_for_status()

            # 生成文件名
            filename = f"styles_{i}.css"
            filepath = f'assets/css/{filename}'

            # 保存 CSS 文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(css_response.text)

            print(f"   ✅ 已保存到 {filepath} ({len(css_response.text)} 字符)")

            extracted_css.append({
                'url': css_url,
                'filename': filename,
                'size': len(css_response.text)
            })

        except Exception as e:
            print(f"   ❌ 下载失败: {e}")

    # 查找内联样式 (<style> 标签)
    print("\n" + "=" * 60)
    print("提取内联样式")
    print("=" * 60)

    style_tags = soup.find_all('style')
    print(f"\n发现 {len(style_tags)} 个内联样式标签\n")

    for i, style in enumerate(style_tags, 1):
        css_content = style.get_text().strip()

        if css_content:
            filename = f"inline_{i}.css"
            filepath = f'assets/css/{filename}'

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(css_content)

            print(f"{i}. 已保存内联样式到 {filepath} ({len(css_content)} 字符)")

            extracted_css.append({
                'type': 'inline',
                'filename': filename,
                'size': len(css_content)
            })

    # 分析 CSS 内容
    print("\n" + "=" * 60)
    print("分析 CSS 内容")
    print("=" * 60)

    total_css_size = 0
    gradient_count = 0
    animation_count = 0
    transition_count = 0
    backdrop_count = 0

    for css_info in extracted_css:
        filepath = f"assets/css/{css_info['filename']}"
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                css_content = f.read()

            total_css_size += len(css_content)

            # 统计关键样式
            gradient_count += css_content.lower().count('gradient')
            animation_count += css_content.lower().count('@keyframes') + css_content.lower().count('animation')
            transition_count += css_content.lower().count('transition')
            backdrop_count += css_content.lower().count('backdrop-filter')

    print(f"\n总 CSS 大小: {total_css_size:,} 字符")
    print(f"渐变背景: {gradient_count} 处")
    print(f"动画定义: {animation_count} 处")
    print(f"过渡效果: {transition_count} 处")
    print(f"磨砂效果: {backdrop_count} 处")

    # 保存分析结果
    import json
    analysis = {
        'total_css_files': len(extracted_css),
        'total_css_size': total_css_size,
        'gradient_count': gradient_count,
        'animation_count': animation_count,
        'transition_count': transition_count,
        'backdrop_count': backdrop_count,
        'extracted_files': extracted_css
    }

    with open('assets/css_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("✅ CSS 提取完成")
    print("=" * 60)
    print(f"分析结果已保存到: assets/css_analysis.json")

if __name__ == "__main__":
    extract_css_files()
