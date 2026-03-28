#!/usr/bin/env python3
"""提取 JavaScript 代码"""

import requests
from bs4 import BeautifulSoup
import re
import os
import json

def extract_javascript():
    """提取 JavaScript 代码"""
    url = "https://www.guowenhuitong.com"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    print("=" * 60)
    print("提取 JavaScript 代码")
    print("=" * 60)

    # 获取网页内容
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 创建保存 JS 的目录
    os.makedirs('assets/js', exist_ok=True)

    # 查找所有 <script src=""> 标签
    script_links = soup.find_all('script', src=True)

    print(f"\n发现 {len(script_links)} 个 JavaScript 文件链接\n")

    extracted_js = []

    for i, script in enumerate(script_links[:15], 1):  # 只取前 15 个
        src = script.get('src', '')
        print(f"{i}. {src[:80]}...")

        # 构建完整的 URL
        if src.startswith('//'):
            js_url = 'https:' + src
        elif src.startswith('/'):
            js_url = url + src
        elif src.startswith('http'):
            js_url = src
        else:
            print(f"   ⚠️  跳过")
            continue

        # 下载 JS 文件
        try:
            js_response = requests.get(js_url, headers=headers, timeout=10)
            js_response.raise_for_status()

            # 生成文件名
            filename = f"script_{i}.js"
            filepath = f'assets/js/{filename}'

            # 保存 JS 文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(js_response.text)

            print(f"   ✅ 已保存 ({len(js_response.text)} 字符)")

            extracted_js.append({
                'url': js_url,
                'filename': filename,
                'size': len(js_response.text)
            })

        except Exception as e:
            print(f"   ❌ 下载失败: {e}")

    # 查找内联脚本 (<script> 标签内容)
    print("\n" + "=" * 60)
    print("提取内联脚本")
    print("=" * 60)

    inline_scripts = soup.find_all('script')
    print(f"\n发现 {len(inline_scripts)} 个脚本标签\n")

    inline_count = 0
    for i, script in enumerate(inline_scripts, 1):
        js_content = script.get_text().strip()

        if js_content and not script.get('src'):  # 只处理内联的
            filename = f"inline_{inline_count + 1}.js"
            filepath = f'assets/js/{filename}'

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(js_content)

            print(f"{i}. 已保存内联脚本到 {filepath} ({len(js_content)} 字符)")

            extracted_js.append({
                'type': 'inline',
                'filename': filename,
                'size': len(js_content)
            })

            inline_count += 1

            if inline_count >= 3:  # 只保存前 3 个内联脚本
                break

    # 分析 JavaScript 内容
    print("\n" + "=" * 60)
    print("分析 JavaScript 内容")
    print("=" * 60)

    total_js_size = sum(js['size'] for js in extracted_js)
    print(f"\n总 JavaScript 大小: {total_js_size:,} 字符")

    # 查找关键功能
    key_features = {
        'animate': 0,
        'animation': 0,
        'hover': 0,
        'scroll': 0,
        'transition': 0,
        'gradient': 0,
        'backdrop': 0,
    }

    for js_info in extracted_js:
        if js_info.get('type') == 'inline':
            continue

        filepath = f"assets/js/{js_info['filename']}"
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                js_content = f.read()

            for feature in key_features:
                key_features[feature] += js_content.lower().count(feature)

    print("\n关键功能统计:")
    for feature, count in key_features.items():
        print(f"  - {feature}: {count} 次")

    # 保存分析结果
    analysis = {
        'total_js_files': len(extracted_js),
        'total_js_size': total_js_size,
        'key_features': key_features,
        'extracted_files': extracted_js
    }

    with open('assets/js_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("✅ JavaScript 提取完成")
    print("=" * 60)
    print("分析结果已保存到: assets/js_analysis.json")

if __name__ == "__main__":
    extract_javascript()
