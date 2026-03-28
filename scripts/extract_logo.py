#!/usr/bin/env python3
"""提取真正的 Logo URL"""

import requests
from bs4 import BeautifulSoup
import re

def extract_logo_url():
    """提取 Logo URL"""
    url = "https://www.guowenhuitong.com"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有 img 标签
        img_tags = soup.find_all('img')

        print(f"找到 {len(img_tags)} 个图片标签\n")

        for i, img in enumerate(img_tags, 1):
            src = img.get('src', '')
            alt = img.get('alt', '')
            class_name = img.get('class', [])

            # 打印图片信息
            print(f"{i}. src: {src}")
            print(f"   alt: {alt}")
            print(f"   class: {class_name}")

            # 查找可能的 Logo
            if 'logo' in src.lower() or 'logo' in alt.lower() or 'logo' in ' '.join(class_name).lower():
                print(f"   *** 可能是 Logo! ***")
            print()

        # 查找 Logo
        logo_url = None
        for img in img_tags:
            src = img.get('src', '')
            alt = img.get('alt', '')
            class_name = img.get('class', [])

            if 'logo' in src.lower() or 'logo' in alt.lower() or 'logo' in ' '.join(class_name).lower():
                logo_url = src
                if not logo_url.startswith('http'):
                    if logo_url.startswith('//'):
                        logo_url = 'https:' + logo_url
                    elif logo_url.startswith('/'):
                        logo_url = url + logo_url
                break

        if logo_url:
            print(f"\n找到 Logo URL: {logo_url}")

            # 下载 Logo
            logo_response = requests.get(logo_url, headers=headers, timeout=10)
            logo_response.raise_for_status()

            # 保存到本地
            with open('assets/logo.png', 'wb') as f:
                f.write(logo_response.content)

            print(f"Logo 已保存到 assets/logo.png ({len(logo_response.content)} 字节)")

            # 检查文件类型
            with open('assets/logo.png', 'rb') as f:
                header = f.read(8)
                if header.startswith(b'\x89PNG'):
                    print("文件类型: PNG")
                elif header.startswith(b'\xFF\xD8'):
                    print("文件类型: JPEG")
                elif header.startswith(b'GIF8'):
                    print("文件类型: GIF")
                elif header.startswith(b'BM'):
                    print("文件类型: BMP")
                else:
                    print(f"文件类型: 未知 (header: {header[:8].hex()})")
        else:
            print("\n未找到 Logo")

    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    extract_logo_url()
