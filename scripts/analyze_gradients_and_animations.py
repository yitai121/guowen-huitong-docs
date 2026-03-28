#!/usr/bin/env python3
"""分析渐变背景和动画效果"""

import re
import json

def analyze_css_file(filepath):
    """分析单个 CSS 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找渐变背景
    gradients = re.findall(r'background\s*:\s*(linear-gradient|radial-gradient)[^;]+;', content, re.IGNORECASE)

    # 查找动画定义
    keyframes = re.findall(r'@keyframes\s+(\w+)\s*\{([^}]+)\}', content, re.IGNORECASE)

    # 查找过渡效果
    transitions = re.findall(r'transition\s*:\s*([^;]+);', content, re.IGNORECASE)

    # 查找悬停效果
    hovers = re.findall(r':hover\s*{([^}]+)}', content, re.IGNORECASE)

    return {
        'gradients': gradients[:20],  # 只取前 20 个
        'keyframes': keyframes[:10],  # 只取前 10 个
        'transitions': transitions[:20],
        'hovers': hovers[:20]
    }

def main():
    print("=" * 60)
    print("分析渐变背景和动画效果")
    print("=" * 60)

    # 分析主要的 CSS 文件
    css_files = [
        'assets/css/styles_2.css',  # 基础样式
        'assets/css/styles_6.css',  # 动画
        'assets/css/styles_4.css',  # 主题
    ]

    all_gradients = []
    all_keyframes = []
    all_transitions = []
    all_hovers = []

    for css_file in css_files:
        print(f"\n分析 {css_file}...")
        analysis = analyze_css_file(css_file)

        print(f"  - 渐变: {len(analysis['gradients'])}")
        print(f"  - 动画: {len(analysis['keyframes'])}")
        print(f"  - 过渡: {len(analysis['transitions'])}")
        print(f"  - 悬停: {len(analysis['hovers'])}")

        all_gradients.extend(analysis['gradients'])
        all_keyframes.extend(analysis['keyframes'])
        all_transitions.extend(analysis['transitions'])
        all_hovers.extend(analysis['hovers'])

    # 提取关键信息
    print("\n" + "=" * 60)
    print("关键发现")
    print("=" * 60)

    print(f"\n1. 渐变背景示例 (共 {len(all_gradients)} 处):")
    for i, gradient in enumerate(all_gradients[:5], 1):
        print(f"   {i}. {gradient[:100]}...")

    print(f"\n2. 动画定义示例 (共 {len(all_keyframes)} 个):")
    for i, (name, code) in enumerate(all_keyframes[:5], 1):
        print(f"   {i}. @keyframes {name}")

    print(f"\n3. 过渡效果示例 (共 {len(all_transitions)} 处):")
    for i, transition in enumerate(all_transitions[:5], 1):
        print(f"   {i}. {transition[:80]}...")

    print(f"\n4. 悬停效果示例 (共 {len(all_hovers)} 处):")
    for i, hover in enumerate(all_hovers[:5], 1):
        print(f"   {i}. {hover[:80]}...")

    # 保存分析结果
    result = {
        'total_gradients': len(all_gradients),
        'total_keyframes': len(all_keyframes),
        'total_transitions': len(all_transitions),
        'total_hovers': len(all_hovers),
        'gradient_examples': all_gradients[:10],
        'keyframe_names': [name for name, _ in all_keyframes[:20]],
        'transition_examples': all_transitions[:10]
    }

    with open('assets/css_effects_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("✅ 分析完成")
    print("=" * 60)
    print("结果已保存到: assets/css_effects_analysis.json")

if __name__ == "__main__":
    main()
