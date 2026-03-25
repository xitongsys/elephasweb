#!/usr/bin/env python3
"""
验证生成的HTML文件
"""

import os
from pathlib import Path

DIST_DIR = Path(__file__).parent / "dist"

def check_file(path):
    """检查HTML文件基本结构"""
    print(f"检查: {path.name}")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = [
        ("DOCTYPE声明", "<!DOCTYPE html>" in content),
        ("html标签", "<html" in content and "</html>" in content),
        ("head标签", "<head" in content and "</head>" in content),
        ("body标签", "<body" in content and "</body>" in content),
        ("header组件", 'class="header"' in content),
        ("modal组件", '合格投资者认证' in content),
        ("footer组件", 'COPYRIGHT©2022 Elephas Investment' in content),
    ]

    all_ok = True
    for check_name, check_result in checks:
        status = "✓" if check_result else "✗"
        print(f"  {status} {check_name}")
        if not check_result:
            all_ok = False

    return all_ok

def main():
    """主函数"""
    print("验证生成的HTML文件...")

    if not DIST_DIR.exists():
        print("错误: dist目录不存在，请先运行build.py")
        return

    html_files = list(DIST_DIR.glob("*.html"))
    if not html_files:
        print("错误: 没有找到HTML文件")
        return

    all_passed = True
    for html_file in html_files:
        if not check_file(html_file):
            all_passed = False
        print()

    if all_passed:
        print("所有检查通过！")
    else:
        print("一些检查失败。")

    # 检查资源文件
    print("\n检查资源文件...")
    required_dirs = ["css", "js", "assets/images"]
    for dir_name in required_dirs:
        dir_path = DIST_DIR / dir_name
        if dir_path.exists():
            print(f"  ✓ {dir_name} 目录存在")
        else:
            print(f"  ✗ {dir_name} 目录不存在")
            all_passed = False

    return all_passed

if __name__ == "__main__":
    main()