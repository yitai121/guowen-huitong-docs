#!/usr/bin/env python3
"""修复加载动画问题"""

# 读取当前 index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到加载动画的 JavaScript 代码
old_script = '''        // 加载动画
        window.addEventListener('load', () => {
            const loader = document.getElementById('loader');
            const progressFill = document.getElementById('progressFill');
            
            // 模拟加载进度
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);
                    setTimeout(() => {
                        loader.classList.add('hidden');
                    }, 300);
                }
                progressFill.style.width = progress + '%';
            }, 100);
        });'''

# 修复后的代码 - 使用 DOMContentLoaded 并添加超时保护
new_script = '''        // 加载动画修复
        (function() {
            const loader = document.getElementById('loader');
            const progressFill = document.getElementById('progressFill');
            
            if (!loader || !progressFill) {
                console.error('加载动画元素未找到');
                return;
            }

            let progress = 0;
            let loaderHidden = false;

            // 隐藏加载动画的函数
            function hideLoader() {
                if (loaderHidden) return;
                loaderHidden = true;
                progress = 100;
                progressFill.style.width = '100%';
                setTimeout(() => {
                    loader.style.opacity = '0';
                    loader.style.visibility = 'hidden';
                    document.body.style.overflow = 'auto';
                }, 300);
            }

            // 模拟加载进度
            const interval = setInterval(() => {
                if (loaderHidden) {
                    clearInterval(interval);
                    return;
                }
                progress += Math.random() * 15;
                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);
                }
                progressFill.style.width = progress + '%';
            }, 100);

            // 方法1: 使用 DOMContentLoaded（更快）
            document.addEventListener('DOMContentLoaded', () => {
                console.log('DOM 加载完成');
                setTimeout(hideLoader, 1000);
            });

            // 方法2: 超时保护（5秒后强制隐藏）
            setTimeout(() => {
                console.log('超时保护触发');
                hideLoader();
            }, 5000);

            // 方法3: window load 作为备用
            window.addEventListener('load', () => {
                console.log('Window 加载完成');
                hideLoader();
            });
        })();'''

# 替换
content = content.replace(old_script, new_script)

# 保存修复后的文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 加载动画问题已修复！")
print("修复内容：")
print("1. 使用 DOMContentLoaded 替代 window.load（更快触发）")
print("2. 添加 5 秒超时保护（防止无限加载）")
print("3. 添加错误处理和日志")
print("4. 确保 body 可以滚动")
